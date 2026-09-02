import os
import time
import argparse

from collections import defaultdict, deque

from docplex.mp.model import Model
from docplex.mp.constants import WriteLevel



# ============================================================
# DATA READERS
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

    for edge_id in range(num_edges):

        if idx >= len(lines):
            raise ValueError(
                f"Unexpected EOF while reading precedence edges in {file_path}"
            )

        data = list(map(int, lines[idx].split()))

        if len(data) != 2:
            raise ValueError(
                f"Invalid precedence edge at line {idx + 1}: {lines[idx]}"
            )

        u, v = data

        if not (0 <= u < num_operations):
            raise ValueError(
                f"Invalid operation {u} in edge ({u}, {v})"
            )

        if not (0 <= v < num_operations):
            raise ValueError(
                f"Invalid operation {v} in edge ({u}, {v})"
            )

        precedence_list.append((u, v))
        idx += 1

    request_list = []

    for op in range(num_operations):

        if idx >= len(lines):
            raise ValueError(
                f"Unexpected EOF while reading operation {op}"
            )

        data = list(map(int, lines[idx].split()))
        idx += 1

        if not data:
            raise ValueError(
                f"Empty operation description for operation {op}"
            )

        num_resources = data[0]
        expected_length = 1 + 2 * num_resources

        if len(data) != expected_length:
            raise ValueError(
                f"Invalid operation {op}: "
                f"expected {expected_length} integers, got {len(data)}"
            )

        map_machine = {}

        for i in range(num_resources):

            machine = data[1 + 2 * i]
            process_time = data[2 + 2 * i]

            if not (0 <= machine < num_machines):
                raise ValueError(
                    f"Invalid machine {machine} for operation {op}"
                )

            if process_time <= 0:
                raise ValueError(
                    f"Invalid processing time {process_time} "
                    f"for operation {op}"
                )

            map_machine[machine] = process_time

        sorted_map = dict(
            sorted(map_machine.items(), key=lambda x: x[1])
        )

        request_list.append(sorted_map)

    # --------------------------------------------------------
    # Find connected components = jobs
    # --------------------------------------------------------

    parent = list(range(num_operations))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            parent[root_b] = root_a

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


def validate_linear_graph(
    num_operations,
    precedence_list,
    job_of,
    num_jobs
):
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)

    for u, v in precedence_list:

        out_degree[u] += 1
        in_degree[v] += 1

        if job_of[u] != job_of[v]:
            raise ValueError(
                f"Edge ({u}, {v}) crosses jobs"
            )

    for op in range(num_operations):

        if out_degree[op] > 1:
            raise ValueError(
                f"Operation {op} has "
                f"{out_degree[op]} successors"
            )

        if in_degree[op] > 1:
            raise ValueError(
                f"Operation {op} has "
                f"{in_degree[op]} predecessors"
            )

    job_op_count = defaultdict(int)

    for op in range(num_operations):
        job_op_count[job_of[op]] += 1

    job_edge_count = defaultdict(int)

    for u, v in precedence_list:
        job_edge_count[job_of[u]] += 1

    for j_id in range(num_jobs):

        n_ops = job_op_count[j_id]
        n_edges = job_edge_count[j_id]

        expected_edges = max(n_ops - 1, 0)

        if n_edges != expected_edges:
            raise ValueError(
                f"Job {j_id} is not a linear chain"
            )


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
                f"Invalid flexibility format"
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

            map_machine = {}

            for _ in range(num_choices):

                machine = data[ptr]
                process_time = data[ptr + 1]

                ptr += 2

                map_machine[machine] = process_time

            sorted_map = dict(
                sorted(
                    map_machine.items(),
                    key=lambda x: x[1]
                )
            )

            request_list.append(sorted_map)

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
        num_factories
    )


def read_flexibility_format(file_path):
    return read_job_format(
        file_path,
        is_flexibility=True
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Can not find file: {file_path}"
        )

    file_path_lower = file_path.lower()

    if "flexibilitydata" in file_path_lower:

        return read_flexibility_format(file_path)

    elif (
        "brandimarte" in file_path_lower
        or "fmj" in file_path_lower
        or "yfjs" in file_path_lower
        or "dafjs" in file_path_lower
    ):

        (
            n_ops,
            n_mac,
            prec,
            req,
            n_jobs,
            j_of,
            _
        ) = read_edge_format(file_path)

        validate_linear_graph(
            n_ops,
            prec,
            j_of,
            n_jobs
        )

        return (
            n_ops,
            n_mac,
            prec,
            req,
            n_jobs,
            j_of,
            None
        )

    else:

        (
            n_ops,
            n_mac,
            prec,
            req,
            n_jobs,
            j_of,
            _
        ) = read_job_format(file_path)

        validate_linear_graph(
            n_ops,
            prec,
            j_of,
            n_jobs
        )

        return (
            n_ops,
            n_mac,
            prec,
            req,
            n_jobs,
            j_of,
            None
        )


# ============================================================
# EXTRACT FIRST / LAST OPERATIONS
# ============================================================

def extract_data(num_operations, precedence_list):

    in_degree = {
        i: 0
        for i in range(num_operations)
    }

    out_degree = {
        i: 0
        for i in range(num_operations)
    }

    for u, v in precedence_list:

        in_degree[v] += 1
        out_degree[u] += 1

    first_ops = [
        i
        for i in range(num_operations)
        if in_degree[i] == 0
    ]

    last_ops = [
        i
        for i in range(num_operations)
        if out_degree[i] == 0
    ]

    return first_ops, last_ops


# ============================================================
# GREEDY SOLVER
# ============================================================

def greedy_solve(
    num_ops,
    num_machines,
    num_factories,
    precedence_list,
    request_list,
    job_of,
    num_jobs
):

    # --------------------------------------------------------
    # Group operations by job
    # --------------------------------------------------------

    job_ops = defaultdict(list)

    for op, j_id in job_of.items():
        job_ops[j_id].append(op)

    # --------------------------------------------------------
    # Job workload
    # --------------------------------------------------------

    job_workload = {}

    for j_id in range(num_jobs):

        job_workload[j_id] = sum(
            min(request_list[op].values())
            for op in job_ops[j_id]
        )

    # --------------------------------------------------------
    # Assign jobs to factories
    # LPT rule
    # --------------------------------------------------------

    sorted_jobs = sorted(
        range(num_jobs),
        key=lambda j: job_workload[j],
        reverse=True
    )

    factory_workload = [
        0
        for _ in range(num_factories)
    ]

    job_factory = {}

    for j_id in sorted_jobs:

        min_f = min(
            range(num_factories),
            key=lambda f: factory_workload[f]
        )

        job_factory[j_id] = min_f

        factory_workload[min_f] += (
            job_workload[j_id]
        )

    # --------------------------------------------------------
    # Build precedence graph
    # --------------------------------------------------------

    adj = defaultdict(list)
    preds = defaultdict(list)

    in_degree = [0] * num_ops

    p_min = [
        min(request_list[i].values())
        for i in range(num_ops)
    ]

    for u, v in precedence_list:

        adj[u].append(v)
        preds[v].append(u)

        in_degree[v] += 1

    # --------------------------------------------------------
    # Topological order
    # --------------------------------------------------------

    queue = deque([
        i
        for i in range(num_ops)
        if in_degree[i] == 0
    ])

    topo_order = []

    in_degree_copy = list(in_degree)

    while queue:

        u = queue.popleft()

        topo_order.append(u)

        for v in adj[u]:

            in_degree_copy[v] -= 1

            if in_degree_copy[v] == 0:
                queue.append(v)

    if len(topo_order) != num_ops:
        raise ValueError(
            "Precedence graph contains a cycle"
        )

    # --------------------------------------------------------
    # Critical tail priority
    # --------------------------------------------------------

    tail_length = {
        i: p_min[i]
        for i in range(num_ops)
    }

    for u in reversed(topo_order):

        if adj[u]:

            tail_length[u] = (
                p_min[u]
                + max(
                    tail_length[v]
                    for v in adj[u]
                )
            )

    # --------------------------------------------------------
    # Schedule
    # --------------------------------------------------------

    machine_avail = defaultdict(
        lambda: defaultdict(int)
    )

    op_end_time = {}

    schedule = {}

    ready_ops = [
        i
        for i in range(num_ops)
        if in_degree[i] == 0
    ]

    while ready_ops:

        ready_ops.sort(
            key=lambda op: tail_length[op],
            reverse=True
        )

        u = ready_ops.pop(0)

        j_id = job_of[u]

        factory = job_factory[j_id]

        ready_time = max(
            [
                op_end_time[p]
                for p in preds[u]
            ],
            default=0
        )

        best_machine = None
        best_start = float("inf")
        best_end = float("inf")

        for k, p_uk in request_list[u].items():

            avail_k = machine_avail[factory][k]

            start_t = max(
                ready_time,
                avail_k
            )

            end_t = start_t + p_uk

            if end_t < best_end:

                best_end = end_t
                best_start = start_t
                best_machine = k

        schedule[u] = {

            "factory": factory,

            "machine": best_machine,

            "start": best_start,

            "duration":
                request_list[u][best_machine],

            "end": best_end
        }

        op_end_time[u] = best_end

        machine_avail[factory][best_machine] = (
            best_end
        )

        for v in adj[u]:

            in_degree[v] -= 1

            if in_degree[v] == 0:
                ready_ops.append(v)

    makespan = max(
        info["end"]
        for info in schedule.values()
    ) if schedule else 0

    return makespan, schedule


# ============================================================
# MODEL 1
# ============================================================

def solve_model_1(
    num_operations,
    num_machines,
    precedence_list,
    request_list,
    num_jobs,
    job_of,
    num_factories,
    greedy_ub,
    greedy_schedule,
    first_ops,
    last_ops,
    threads=None,
    log_output=True
):

    operations = range(num_operations)
    machines = range(num_machines)
    factories = range(num_factories)
    jobs = range(num_jobs)

    # ========================================================
    # IMPORTANT:
    # Use greedy solution as valid horizon
    # ========================================================

    UB = greedy_ub

    print("\n" + "=" * 70)
    print("MODEL 1 PARAMETERS")
    print("=" * 70)

    print(f"Greedy UB = {UB}")
    print(f"First operations = {len(first_ops)}")
    print(f"Last operations  = {len(last_ops)}")

    mdl = Model(
        name="DFJSP_Model_1"
    )

    # ========================================================
    # VARIABLES
    # ========================================================

    # --------------------------------------------------------
    # Z[j,f]
    # --------------------------------------------------------

    Z = mdl.binary_var_dict(
        [
            (j, f)
            for j in jobs
            for f in factories
        ],
        name="Z"
    )

    # --------------------------------------------------------
    # X[o,f,k]
    # --------------------------------------------------------

    X = {}

    for o in operations:

        for f in factories:

            for k in request_list[o]:

                X[o, f, k] = mdl.binary_var(
                    name=f"X_{o}_{f}_{k}"
                )

    # --------------------------------------------------------
    # Y[o1,o2,f,k]
    # --------------------------------------------------------

    Y = {}

    for o1 in operations:

        for o2 in range(
            o1 + 1,
            num_operations
        ):

            common_machines = (
                set(request_list[o1])
                & set(request_list[o2])
            )

            for f in factories:

                for k in common_machines:

                    Y[o1, o2, f, k] = (
                        mdl.binary_var(
                            name=(
                                f"Y_{o1}_{o2}_{f}_{k}"
                            )
                        )
                    )

    # --------------------------------------------------------
    # B[o]
    # Start time
    # --------------------------------------------------------

    B = mdl.continuous_var_dict(
        operations,
        lb=0,
        ub=UB,
        name="B"
    )

    # --------------------------------------------------------
    # Cmax
    # --------------------------------------------------------

    Cmax = mdl.continuous_var(
        lb=0,
        ub=UB,
        name="Cmax"
    )

    # ========================================================
    # OBJECTIVE
    # ========================================================

    mdl.minimize(Cmax)

    # ========================================================
    # (1) FACTORY ASSIGNMENT
    #
    # sum_f Z[j,f] = 1
    # ========================================================

    for j in jobs:

        mdl.add_constraint(

            mdl.sum(
                Z[j, f]
                for f in factories
            ) == 1,

            ctname=f"assign_factory_{j}"
        )

    # ========================================================
    # (2) MACHINE ASSIGNMENT
    #
    # sum_k X[o,f,k] = Z[j(o),f]
    # ========================================================

    for o in operations:

        j = job_of[o]

        for f in factories:

            mdl.add_constraint(

                mdl.sum(
                    X[o, f, k]
                    for k in request_list[o]
                )
                == Z[j, f],

                ctname=f"assign_machine_{o}_{f}"
            )

    # ========================================================
    # (3) PRECEDENCE
    # ========================================================

    for u, v in precedence_list:

        duration_u = mdl.sum(

            request_list[u][k]
            * X[u, f, k]

            for f in factories
            for k in request_list[u]
        )

        mdl.add_constraint(

            B[v]
            >= B[u] + duration_u,

            ctname=f"precedence_{u}_{v}"
        )

    # ========================================================
    # (4)-(5) NON-OVERLAP
    # ========================================================

    for o1 in operations:

        for o2 in range(
            o1 + 1,
            num_operations
        ):

            common_machines = (
                set(request_list[o1])
                & set(request_list[o2])
            )

            if not common_machines:
                continue

            for f in factories:

                for k in common_machines:

                    y = Y[o1, o2, f, k]

                    x1 = X[o1, f, k]
                    x2 = X[o2, f, k]

                    p1 = request_list[o1][k]
                    p2 = request_list[o2][k]

                    # ----------------------------------------
                    # o1 before o2
                    #
                    # Active when:
                    # x1 = 1
                    # x2 = 1
                    # y = 1
                    # ----------------------------------------

                    mdl.add_constraint(

                        B[o2]
                        >= B[o1]
                        + p1
                        - UB * (
                            3 - x1 - x2 - y
                        ),

                        ctname=(
                            f"no_overlap_1_"
                            f"{o1}_{o2}_{f}_{k}"
                        )
                    )

                    # ----------------------------------------
                    # o2 before o1
                    #
                    # Active when:
                    # x1 = 1
                    # x2 = 1
                    # y = 0
                    # ----------------------------------------

                    mdl.add_constraint(

                        B[o1]
                        >= B[o2]
                        + p2
                        - UB * (
                            2 - x1 - x2 + y
                        ),

                        ctname=(
                            f"no_overlap_2_"
                            f"{o1}_{o2}_{f}_{k}"
                        )
                    )

    # ========================================================
    # MAKESPAN
    #
    # Only last operations are necessary
    # ========================================================

    for o in last_ops:

        duration_o = mdl.sum(

            request_list[o][k]
            * X[o, f, k]

            for f in factories
            for k in request_list[o]
        )

        mdl.add_constraint(

            Cmax >= B[o] + duration_o,

            ctname=f"makespan_{o}"
        )

    # ========================================================
    # OPTIONAL:
    # FIX FIRST OPERATIONS LB
    #
    # Do NOT fix them to zero.
    # Just redundant explicit lower bound.
    # ========================================================

    for o in first_ops:

        mdl.add_constraint(
            B[o] >= 0,
            ctname=f"first_op_lb_{o}"
        )

    # ========================================================
    # MACHINE LOAD LOWER BOUND
    # ========================================================

    for f in factories:

        for k in machines:

            load_expr = mdl.sum(

                request_list[o][k]
                * X[o, f, k]

                for o in operations
                if k in request_list[o]
            )

            if load_expr.number_of_terms() > 0:

                mdl.add_constraint(

                    Cmax >= load_expr,

                    ctname=(
                        f"machine_load_{f}_{k}"
                    )
                )

    # ========================================================
    # MIP START FROM GREEDY
    # ========================================================

    print("\nAdding greedy MIP start...")

    mip_start = mdl.new_solution()

    # --------------------------------------------------------
    # Z variables
    # --------------------------------------------------------

    for j in jobs:

        # Find factory from any operation
        job_operations = [
            o
            for o in operations
            if job_of[o] == j
        ]

        factory = greedy_schedule[
            job_operations[0]
        ]["factory"]

        for f in factories:

            value = 1 if f == factory else 0

            mip_start.add_var_value(
                Z[j, f],
                value
            )

    # --------------------------------------------------------
    # X variables
    # --------------------------------------------------------

    for o in operations:

        selected_factory = (
            greedy_schedule[o]["factory"]
        )

        selected_machine = (
            greedy_schedule[o]["machine"]
        )

        for f in factories:

            for k in request_list[o]:

                value = int(
                    f == selected_factory
                    and k == selected_machine
                )

                mip_start.add_var_value(
                    X[o, f, k],
                    value
                )

    # --------------------------------------------------------
    # B variables
    # --------------------------------------------------------

    for o in operations:

        mip_start.add_var_value(

            B[o],

            greedy_schedule[o]["start"]
        )

    # --------------------------------------------------------
    # Cmax
    # --------------------------------------------------------

    mip_start.add_var_value(
        Cmax,
        greedy_ub
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Y variables
    #
    # Determine ordering from greedy schedule
    # --------------------------------------------------------

    for (o1, o2, f, k), y_var in Y.items():

        s1 = greedy_schedule[o1]
        s2 = greedy_schedule[o2]

        same_resource = (
            s1["factory"] == f
            and s2["factory"] == f
            and s1["machine"] == k
            and s2["machine"] == k
        )

        if same_resource:

            value = int(
                s1["start"] <= s2["start"]
            )

        else:

            value = 0

        mip_start.add_var_value(
            y_var,
            value
        )

    # --------------------------------------------------------
    # Add MIP start
    # --------------------------------------------------------

    mdl.add_mip_start(
        mip_start,
        write_level=WriteLevel.AllVars
    )



    # ========================================================
    # STATISTICS
    # ========================================================

    print("\n" + "=" * 70)
    print("MODEL STATISTICS")
    print("=" * 70)

    print(
        f"Variables    : "
        f"{mdl.number_of_variables}"
    )

    print(
        f"Constraints : "
        f"{mdl.number_of_constraints}"
    )

    print(f"Greedy UB   : {greedy_ub}")

    # ========================================================
    # SOLVE
    # ========================================================

    print("\n" + "=" * 70)
    print("START CPLEX")
    print("=" * 70)

    start_time = time.time()
    
    solution = mdl.solve(
        log_output=log_output    )

    elapsed_time = time.time() - start_time

    # ========================================================
    # RESULT
    # ========================================================

    details = mdl.solve_details

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)

    print(f"Status     : {details.status}")
    print(f"Time       : {elapsed_time:.3f}")

    if solution is None:

        print("No solution found")

        return None

    objective = solution.objective_value

    print(f"Makespan   : {objective:.6f}")
    print(f"Best bound : {details.best_bound:.6f}")

    if details.mip_relative_gap is not None:

        print(
            f"Gap        : "
            f"{details.mip_relative_gap * 100:.4f}%"
        )

    # ========================================================
    # EXTRACT SOLUTION
    # ========================================================

    result_schedule = {}

    for o in operations:

        selected_factory = None
        selected_machine = None

        for f in factories:

            for k in request_list[o]:

                if solution.get_value(
                    X[o, f, k]
                ) > 0.5:

                    selected_factory = f
                    selected_machine = k

        start = solution.get_value(B[o])

        duration = request_list[o][
            selected_machine
        ]

        result_schedule[o] = {

            "job": job_of[o],

            "factory": selected_factory,

            "machine": selected_machine,

            "start": start,

            "duration": duration,

            "end": start + duration
        }

    return {

        "model": mdl,

        "solution": solution,

        "makespan": objective,

        "best_bound": details.best_bound,

        "gap": details.mip_relative_gap,

        "solve_time": elapsed_time,

        "greedy_ub": greedy_ub,

        "schedule": result_schedule
    }


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        required=True
    )

    parser.add_argument(
        "--factories",
        type=int,
        default=2
    )

    args = parser.parse_args()

    # ========================================================
    # LOAD DATA
    # ========================================================

    (
        num_operations,
        num_machines,
        precedence_list,
        request_list,
        num_jobs,
        job_of,
        data_num_factories
    ) = load_data(args.input)

    # ========================================================
    # FACTORIES
    # ========================================================

    if data_num_factories is not None:

        num_factories = data_num_factories

    else:

        num_factories = args.factories

    # ========================================================
    # EXTRACT FIRST / LAST OPS
    # ========================================================

    first_ops, last_ops = extract_data(
        num_operations,
        precedence_list
    )

    print("=" * 70)
    print("INSTANCE")
    print("=" * 70)

    print(f"File       : {args.input}")
    print(f"Operations : {num_operations}")
    print(f"Jobs       : {num_jobs}")
    print(f"Machines   : {num_machines}")
    print(f"Factories  : {num_factories}")
    print(f"Edges      : {len(precedence_list)}")

    # ========================================================
    # GREEDY SOLVE
    # ========================================================

    print("\n" + "=" * 70)
    print("GREEDY HEURISTIC")
    print("=" * 70)

    greedy_start = time.time()

    greedy_ub, greedy_schedule = greedy_solve(

        num_ops=num_operations,

        num_machines=num_machines,

        num_factories=num_factories,

        precedence_list=precedence_list,

        request_list=request_list,

        job_of=job_of,

        num_jobs=num_jobs
    )

    greedy_time = time.time() - greedy_start

    print(f"Greedy UB   : {greedy_ub}")
    print(f"Greedy time : {greedy_time:.6f} sec")

    # ========================================================
    # SOLVE MODEL 1
    # ========================================================

    result = solve_model_1(

        num_operations=num_operations,

        num_machines=num_machines,

        precedence_list=precedence_list,

        request_list=request_list,

        num_jobs=num_jobs,

        job_of=job_of,

        num_factories=num_factories,

        greedy_ub=greedy_ub,

        greedy_schedule=greedy_schedule,

        first_ops=first_ops,

        last_ops=last_ops,


        log_output=True
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    if result is not None:

        print("\n" + "=" * 70)
        print("FINAL SUMMARY")
        print("=" * 70)

        print(
            f"Greedy UB : "
            f"{result['greedy_ub']}"
        )

        print(
            f"CPLEX     : "
            f"{result['makespan']:.6f}"
        )

        print(
            f"Bound     : "
            f"{result['best_bound']:.6f}"
        )

        print(
            f"Time      : "
            f"{result['solve_time']:.3f}"
        )


if __name__ == "__main__":
    main()