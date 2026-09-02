import argparse
import os
import time
from collections import defaultdict

from docplex.cp.model import (
    CpoModel,
    interval_var,
    alternative,
    sequence_var,
    no_overlap,
    end_before_start,
    presence_of,
    end_of,
    max as cp_max,
)


# ============================================================
# DATA READING
# Same format as main.txt
# ============================================================

def read_edge_format(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.lstrip().startswith("#")
        ]

    if not lines:
        raise ValueError(f"Empty dataset: {file_path}")

    header = list(map(int, lines[0].split()))

    if len(header) < 3:
        raise ValueError(
            f"Invalid header in {file_path}: {lines[0]}"
        )

    num_operations = header[0]
    num_edges = header[1]
    num_machines = header[2]

    idx = 1
    precedence_list = []

    # --------------------------------------------------------
    # Read precedence edges
    # --------------------------------------------------------

    for _ in range(num_edges):
        if idx >= len(lines):
            raise ValueError(
                f"Unexpected EOF while reading precedence edges"
            )

        data = list(map(int, lines[idx].split()))

        if len(data) != 2:
            raise ValueError(
                f"Invalid precedence edge: {lines[idx]}"
            )

        u, v = data

        if not (0 <= u < num_operations):
            raise ValueError(
                f"Invalid operation {u}"
            )

        if not (0 <= v < num_operations):
            raise ValueError(
                f"Invalid operation {v}"
            )

        precedence_list.append((u, v))
        idx += 1

    # --------------------------------------------------------
    # Read machine alternatives
    # --------------------------------------------------------

    request_list = []

    for op in range(num_operations):

        if idx >= len(lines):
            raise ValueError(
                f"Unexpected EOF while reading operation {op}"
            )

        data = list(map(int, lines[idx].split()))
        idx += 1

        num_resources = data[0]
        expected_length = 1 + 2 * num_resources

        if len(data) != expected_length:
            raise ValueError(
                f"Invalid operation {op}: "
                f"expected {expected_length} integers"
            )

        machine_map = {}

        for i in range(num_resources):

            machine = data[1 + 2 * i]
            process_time = data[2 + 2 * i]

            if not (0 <= machine < num_machines):
                raise ValueError(
                    f"Invalid machine {machine} "
                    f"for operation {op}"
                )

            if process_time <= 0:
                raise ValueError(
                    f"Invalid processing time {process_time}"
                )

            machine_map[machine] = process_time

        request_list.append(
            dict(sorted(machine_map.items()))
        )

    # --------------------------------------------------------
    # Infer jobs using connected components
    # --------------------------------------------------------

    parent = list(range(num_operations))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)

        if ra != rb:
            parent[rb] = ra

    for u, v in precedence_list:
        union(u, v)

    root_to_job = {}
    job_of = {}

    next_job = 0

    for op in range(num_operations):

        root = find(op)

        if root not in root_to_job:
            root_to_job[root] = next_job
            next_job += 1

        job_of[op] = root_to_job[root]

    num_jobs = next_job

    return (
        num_operations,
        num_machines,
        precedence_list,
        request_list,
        num_jobs,
        job_of,
        None,
    )


# ============================================================
# JOB FORMAT
# Brandimarte / Fattahi / Hurink
# ============================================================

def read_job_format(file_path, is_flexibility=False):

    with open(file_path, "r", encoding="utf-8") as f:

        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    if not lines:
        raise ValueError(f"Empty dataset: {file_path}")

    header = list(map(int, lines[0].split()))

    if is_flexibility:

        if len(header) < 3:
            raise ValueError(
                "Expected: num_jobs num_machines num_factories"
            )

        num_jobs = header[0]
        num_machines = header[1]
        num_factories = header[2]

    else:

        num_jobs = header[0]
        num_machines = header[1]
        num_factories = None

    request_list = []
    precedence_list = []
    job_of = {}

    op_id = 0

    for j_id, line in enumerate(lines[1:]):

        data = list(map(int, line.split()))

        num_ops_in_job = data[0]

        ptr = 1

        for k in range(num_ops_in_job):

            num_choices = data[ptr]
            ptr += 1

            machine_map = {}

            for _ in range(num_choices):

                machine = data[ptr]
                process_time = data[ptr + 1]

                ptr += 2

                machine_map[machine] = process_time

            request_list.append(
                dict(sorted(machine_map.items()))
            )

            job_of[op_id] = j_id

            if k > 0:
                precedence_list.append(
                    (op_id - 1, op_id)
                )

            op_id += 1

    num_operations = op_id

    return (
        num_operations,
        num_machines,
        precedence_list,
        request_list,
        num_jobs,
        job_of,
        num_factories,
    )


def load_data(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Cannot find file: {file_path}"
        )

    file_path_lower = file_path.lower()

    if "flexibilitydata" in file_path_lower:

        return read_job_format(
            file_path,
            is_flexibility=True
        )

    # Detect format
    with open(file_path, "r", encoding="utf-8") as f:

        first_line = ""

        for line in f:
            line = line.strip()

            if line and not line.startswith("#"):
                first_line = line
                break

    header = first_line.split()

    # Edge format has 3 numbers:
    # num_operations num_edges num_machines
    #
    # Job format normally has:
    # num_jobs num_machines

    if len(header) >= 3:
        return read_edge_format(file_path)

    return read_job_format(file_path)


# ============================================================
# EXTRACT JOB OPERATIONS
# ============================================================

def get_job_operations(num_jobs, job_of):

    job_operations = defaultdict(list)

    for op, job in job_of.items():
        job_operations[job].append(op)

    return job_operations


# ============================================================
# CP MODEL
# Meng et al. (2020)
# ============================================================

def solve_cp(
    num_operations,
    num_machines,
    num_factories,
    precedence_list,
    request_list,
    num_jobs,
    job_of
):

    mdl = CpoModel("DFJSP_CP_Meng2020")

    # ========================================================
    # Upper bound for interval domains
    #
    # Safe horizon:
    # sum of maximum processing times of all operations
    # ========================================================

    horizon = sum(
        max(request_list[i].values())
        for i in range(num_operations)
    )

    print("=" * 70)
    print("DFJSP CP MODEL - MENG ET AL. (2020)")
    print("=" * 70)

    print(f"Operations : {num_operations}")
    print(f"Jobs       : {num_jobs}")
    print(f"Machines   : {num_machines}")
    print(f"Factories  : {num_factories}")
    print(f"Horizon    : {horizon}")

    # ========================================================
    # 1. Main operation interval
    #
    # ops[i]
    #
    # Corresponds to:
    # ops_{i,j}
    # ========================================================

    ops = {}

    for i in range(num_operations):

        ops[i] = interval_var(
            start=(0, horizon),
            end=(0, horizon),
            name=f"op_{i}"
        )

    # ========================================================
    # 2. Optional mode intervals
    #
    # modes[i,f,k]
    #
    # Each mode corresponds to assigning operation i
    # to machine k in factory f.
    #
    # Processing time is fixed according to p[i,k].
    # ========================================================

    modes = {}

    for i in range(num_operations):

        for f in range(num_factories):

            for k, processing_time in request_list[i].items():

                modes[(i, f, k)] = interval_var(
                    optional=True,
                    size=processing_time,
                    name=f"mode_{i}_{f}_{k}"
                )

    # ========================================================
    # Constraint (37)
    #
    # alternative(
    #     operation,
    #     all feasible factory-machine modes
    # )
    #
    # Exactly one mode must be selected.
    # ========================================================

    for i in range(num_operations):

        alternatives = []

        for f in range(num_factories):

            for k in request_list[i]:

                alternatives.append(
                    modes[(i, f, k)]
                )

        mdl.add(
            alternative(
                ops[i],
                alternatives
            )
        )

    # ========================================================
    # 3. Machine sequences
    #
    # mchs[f,k]
    #
    # Contains all optional intervals that can run
    # on machine k in factory f.
    # ========================================================

    machine_sequences = {}

    for f in range(num_factories):

        for k in range(num_machines):

            machine_intervals = []

            for i in range(num_operations):

                if k in request_list[i]:

                    machine_intervals.append(
                        modes[(i, f, k)]
                    )

            if machine_intervals:

                machine_sequences[(f, k)] = sequence_var(
                    machine_intervals,
                    name=f"seq_f{f}_m{k}"
                )

                # =================================================
                # Constraint (38)
                #
                # noOverlap(mchs[f,k])
                # =================================================

                mdl.add(
                    no_overlap(
                        machine_sequences[(f, k)]
                    )
                )

    # ========================================================
    # Constraint (39)
    #
    # Precedence constraints
    #
    # endBeforeStart(
    #     ops[u],
    #     ops[v]
    # )
    # ========================================================

    for u, v in precedence_list:

        mdl.add(
            end_before_start(
                ops[u],
                ops[v]
            )
        )

    # ========================================================
    # Constraint (40)
    #
    # All operations belonging to the same job
    # must be assigned to the SAME factory.
    #
    # Paper uses presence relationships between
    # factory-specific optional intervals.
    #
    # We implement the equivalent compact form:
    #
    # sum_k presence(mode[i,f,k])
    # ==
    # sum_k presence(mode[j,f,k])
    #
    # for every pair of operations in the same job.
    #
    # Because alternative() guarantees exactly one
    # mode per operation, this means:
    #
    # operation i is in factory f
    # iff
    # operation j is in factory f.
    # ========================================================

    job_operations = get_job_operations(
        num_jobs,
        job_of
    )

    for j in range(num_jobs):

        job_ops = job_operations[j]

        if len(job_ops) <= 1:
            continue

        reference_op = job_ops[0]

        for i in job_ops[1:]:

            for f in range(num_factories):

                reference_presence = sum(
                    presence_of(
                        modes[(reference_op, f, k)]
                    )
                    for k in request_list[reference_op]
                )

                current_presence = sum(
                    presence_of(
                        modes[(i, f, k)]
                    )
                    for k in request_list[i]
                )

                mdl.add(
                    reference_presence
                    ==
                    current_presence
                )

    # ========================================================
    # Makespan
    #
    # Cmax >= endOf(last operation of every job)
    #
    # More generally:
    #
    # Cmax = max end of all operations
    #
    # This is equivalent for precedence-connected jobs.
    # ========================================================

    cmax = cp_max(
        end_of(ops[i])
        for i in range(num_operations)
    )

    mdl.add(
        mdl.minimize(cmax)
    )

    # ========================================================
    # SOLVE
    # ========================================================

    print("\n[*] Starting CP Optimizer...")

    start_time = time.time()

    solution = mdl.solve(
        LogVerbosity="Terse",
        # RestartFailLimit=1000,
        # OptimalityTolerance=0,
        # RelativeOptimalityTolerance=0,
    )

    elapsed = time.time() - start_time

    # ========================================================
    # RESULTS
    # ========================================================

    if solution is None:

        print("\n[!] No solution found")

        return None, None

    makespan = solution.get_objective_values()[0]

    print("\n" + "=" * 70)
    print("SOLUTION FOUND")
    print("=" * 70)

    print(f"Makespan : {makespan}")
    print(f"Time     : {elapsed:.4f} seconds")

    # ========================================================
    # Extract schedule
    # ========================================================

    schedule = {}

    for i in range(num_operations):

        operation_solution = solution.get_var_solution(
            ops[i]
        )

        start = operation_solution.get_start()
        end = operation_solution.get_end()

        assigned_factory = None
        assigned_machine = None

        for f in range(num_factories):

            for k in request_list[i]:

                mode_solution = solution.get_var_solution(
                    modes[(i, f, k)]
                )

                if mode_solution.is_present():

                    assigned_factory = f
                    assigned_machine = k

                    break

            if assigned_factory is not None:
                break

        duration = (
            request_list[i][assigned_machine]
        )

        schedule[i] = {
            "job": job_of[i],
            "factory": assigned_factory,
            "machine": assigned_machine,
            "start": start,
            "end": end,
            "duration": duration,
        }

    return makespan, schedule


# ============================================================
# VERIFY SCHEDULE
# ============================================================

def verify_schedule(
    schedule,
    precedence_list,
    num_jobs,
    num_factories,
):

    print("\n[*] Verifying solution...")

    # --------------------------------------------------------
    # 1. Precedence
    # --------------------------------------------------------

    for u, v in precedence_list:

        if schedule[u]["end"] > schedule[v]["start"]:

            print(
                f"[X] Precedence violation: "
                f"{u} -> {v}"
            )

            return False

    # --------------------------------------------------------
    # 2. Same factory per job
    # --------------------------------------------------------

    job_factories = defaultdict(set)

    for i, info in schedule.items():

        job_factories[info["job"]].add(
            info["factory"]
        )

    for j, factories in job_factories.items():

        if len(factories) != 1:

            print(
                f"[X] Job {j} uses multiple factories: "
                f"{factories}"
            )

            return False

    # --------------------------------------------------------
    # 3. Machine overlap
    # --------------------------------------------------------

    machine_intervals = defaultdict(list)

    for i, info in schedule.items():

        key = (
            info["factory"],
            info["machine"]
        )

        machine_intervals[key].append(
            (
                info["start"],
                info["end"],
                i
            )
        )

    for key, intervals in machine_intervals.items():

        intervals.sort()

        for idx in range(len(intervals) - 1):

            _, end1, op1 = intervals[idx]
            start2, _, op2 = intervals[idx + 1]

            if end1 > start2:

                print(
                    f"[X] Machine overlap: "
                    f"{key}, "
                    f"op {op1} and op {op2}"
                )

                return False

    print("[✓] Schedule is VALID")

    return True


# ============================================================
# PRINT SCHEDULE
# ============================================================

def print_schedule(schedule):

    print("\n" + "=" * 100)

    print(
        f"{'OP':<6}"
        f"{'JOB':<6}"
        f"{'FACTORY':<10}"
        f"{'MACHINE':<10}"
        f"{'START':<10}"
        f"{'END':<10}"
        f"{'DURATION':<10}"
    )

    print("-" * 100)

    for i in sorted(schedule):

        info = schedule[i]

        print(
            f"{i:<6}"
            f"{info['job']:<6}"
            f"{info['factory']:<10}"
            f"{info['machine']:<10}"
            f"{info['start']:<10}"
            f"{info['end']:<10}"
            f"{info['duration']:<10}"
        )

    print("=" * 100)


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="DFJSP CP Optimizer - Meng et al. (2020)"
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=str,
        help="Path to dataset"
    )

    parser.add_argument(
        "--factories",
        "-num_f",
        type=int,
        default=2,
        help="Number of factories"
    )

    parser.add_argument(
        "--time_limit",
        "-t",
        type=int,
        default=600,
        help="Time limit in seconds"
    )

    args = parser.parse_args()

    # ========================================================
    # Load data
    # ========================================================

    print(f"[*] Loading: {args.input}")

    (
        num_operations,
        num_machines,
        precedence_list,
        request_list,
        num_jobs,
        job_of,
        file_factories,
    ) = load_data(args.input)

    if file_factories is not None:

        num_factories = file_factories

    else:

        num_factories = args.factories

    # ========================================================
    # Solve
    # ========================================================

    makespan, schedule = solve_cp(
        num_operations=num_operations,
        num_machines=num_machines,
        num_factories=num_factories,
        precedence_list=precedence_list,
        request_list=request_list,
        num_jobs=num_jobs,
        job_of=job_of    )

    # ========================================================
    # Verify
    # ========================================================

    if schedule is not None:

        # print_schedule(schedule)

        valid = verify_schedule(
            schedule,
            precedence_list,
            num_jobs,
            num_factories,
        )

        print("\n" + "=" * 70)
        print("FINAL RESULT")
        print("=" * 70)

        print(f"Makespan : {makespan}")
        print(
            f"Status    : "
            f"{'VALID' if valid else 'INVALID'}"
        )


if __name__ == "__main__":
    main()