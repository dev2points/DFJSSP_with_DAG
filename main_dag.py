import argparse
from collections import defaultdict, deque
import os
import time
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


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
            raise ValueError(f"Invalid operation {u} in edge ({u}, {v})")

        if not (0 <= v < num_operations):
            raise ValueError(f"Invalid operation {v} in edge ({u}, {v})")

        precedence_list.append((u, v))
        idx += 1

    request_list = []

    for op in range(num_operations):
        if idx >= len(lines):
            raise ValueError(f"Unexpected EOF while reading operation {op}")

        data = list(map(int, lines[idx].split()))
        idx += 1

        if not data:
            raise ValueError(f"Empty operation description for operation {op}")

        num_resources = data[0]
        expected_length = 1 + 2 * num_resources

        if len(data) != expected_length:
            raise ValueError(
                f"Invalid operation {op}: expected {expected_length} integers, got {len(data)}\n"
                f"Line: {lines[idx - 1]}"
            )

        map_machine = {}

        for i in range(num_resources):
            machine = data[1 + 2 * i]
            process_time = data[2 + 2 * i]

            if not (0 <= machine < num_machines):
                raise ValueError(
                    f"Invalid machine {machine} for operation {op}. Valid range: 0..{num_machines - 1}"
                )

            if process_time <= 0:
                raise ValueError(
                    f"Invalid processing time {process_time} for operation {op}"
                )

            map_machine[machine] = process_time

        sorted_map = dict(sorted(map_machine.items(), key=lambda x: x[1]))
        request_list.append(sorted_map)

    if idx != len(lines):
        print(f"[Warning] {len(lines) - idx} extra lines at the end of {file_path}")

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

    if len(request_list) != num_operations:
        raise AssertionError(
            f"request_list has {len(request_list)} operations, expected {num_operations}"
        )

    if len(precedence_list) != num_edges:
        raise AssertionError(
            f"precedence_list has {len(precedence_list)} edges, expected {num_edges}"
        )

    return (
        num_operations,
        num_machines,
        precedence_list,
        request_list,
        num_jobs,
        job_of,
        None,
    )


def validate_linear_graph(num_operations, precedence_list, job_of, num_jobs):
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)

    for u, v in precedence_list:
        out_degree[u] += 1
        in_degree[v] += 1

        if job_of[u] != job_of[v]:
            raise ValueError(
                f"Non-linear precedence graph: edge ({u}, {v}) crosses jobs "
                f"{job_of[u]} -> {job_of[v]}. Only supports a linear precedence chain within each job."
            )

    for op in range(num_operations):
        if out_degree[op] > 1:
            raise ValueError(
                f"Non-linear precedence graph: operation {op} has {out_degree[op]} successors."
            )
        if in_degree[op] > 1:
            raise ValueError(
                f"Non-linear precedence graph: operation {op} has {in_degree[op]} predecessors."
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
                f"Non-linear precedence graph: job {j_id} has {n_ops} operations "
                f"but {n_edges} precedence edges (expected {expected_edges} for a linear chain)."
            )


def read_job_format(file_path, is_flexibility=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not lines:
        raise ValueError(f"Empty dataset: {file_path}")

    header = list(map(int, lines[0].split()))

    if is_flexibility:
        if len(header) < 3:
            raise ValueError(
                f"Invalid header in {file_path}: expected [num_jobs, num_machines, num_factories], got: {lines[0]}"
            )
        num_jobs, num_machines, num_factories = header[0], header[1], header[2]
    else:
        num_jobs, num_machines = header[0], header[1]
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

            sorted_map = dict(sorted(map_machine.items(), key=lambda x: x[1]))
            request_list.append(sorted_map)

            job_of[op_id] = j_id

            if k > 0:
                precedence_list.append((op_id - 1, op_id))

            op_id += 1

    num_operations = op_id
    return num_operations, num_machines, precedence_list, request_list, num_jobs, job_of, num_factories


def read_flexibility_format(file_path):
    return read_job_format(file_path, is_flexibility=True)


def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Can not find file: {file_path}")

    file_path_lower = file_path.lower()
    if 'flexibilitydata' in file_path_lower:
        return read_flexibility_format(file_path)
    elif 'brandimarte' in file_path_lower or 'fmj' in file_path_lower or 'yfjs' in file_path_lower or 'dafjs' in file_path_lower:
        n_ops, n_mac, prec, req, n_jobs, j_of, _ = read_edge_format(file_path)
        validate_linear_graph(n_ops, prec, j_of, n_jobs)
        return n_ops, n_mac, prec, req, n_jobs, j_of, None
    else:
        n_ops, n_mac, prec, req, n_jobs, j_of, _ = read_job_format(file_path)
        validate_linear_graph(n_ops, prec, j_of, n_jobs)
        return n_ops, n_mac, prec, req, n_jobs, j_of, None


def extract_data(num_operations, precedence_list):
    in_degree = {i: 0 for i in range(num_operations)}
    out_degree = {i: 0 for i in range(num_operations)}

    for u, v in precedence_list:
        in_degree[v] += 1
        out_degree[u] += 1
    first_ops = [i for i in range(num_operations) if in_degree[i] == 0]
    last_ops = [i for i in range(num_operations) if out_degree[i] == 0]
    return first_ops, last_ops


def compute_E_star(num_ops, precedence_list, request_list):
    p_min = [min(req.values()) for req in request_list]
    
    adj = defaultdict(list)
    in_degree = [0] * num_ops
    for u, v in precedence_list:
        adj[u].append(v)
        in_degree[v] += 1
        
    queue = deque([i for i in range(num_ops) if in_degree[i] == 0])
    topo_order = []
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    dist_dict = defaultdict(dict)
    for u in reversed(topo_order):
        for v in adj[u]:
            if v not in dist_dict[u] or p_min[u] > dist_dict[u][v]:
                dist_dict[u][v] = p_min[u]
            
            for w_node, w_vw in dist_dict[v].items():
                w_uw = p_min[u] + w_vw
                if w_node not in dist_dict[u] or w_uw > dist_dict[u][w_node]:
                    dist_dict[u][w_node] = w_uw
                    
    E_star = {}
    for u, targets in dist_dict.items():
        for v, w in targets.items():
            E_star[(u, v)] = w
            
    return E_star


def greedy_solve(num_ops, num_machines, num_factories, precedence_list, request_list, job_of, num_jobs):
    job_ops = defaultdict(list)
    for op, j_id in job_of.items():
        job_ops[j_id].append(op)

    job_workload = {}
    for j_id in range(num_jobs):
        job_workload[j_id] = sum(min(request_list[op].values()) for op in job_ops[j_id])

    sorted_jobs = sorted(range(num_jobs), key=lambda j: job_workload[j], reverse=True)
    factory_workload = [0] * num_factories
    job_factory = {}

    for j_id in sorted_jobs:
        min_f = min(range(num_factories), key=lambda f: factory_workload[f])
        job_factory[j_id] = min_f
        factory_workload[min_f] += job_workload[j_id]

    adj = defaultdict(list)
    preds = defaultdict(list)
    in_degree = [0] * num_ops
    p_min = [min(request_list[i].values()) for i in range(num_ops)]

    for u, v in precedence_list:
        adj[u].append(v)
        preds[v].append(u)
        in_degree[v] += 1

    queue = deque([i for i in range(num_ops) if in_degree[i] == 0])
    topo_order = []
    in_degree_copy = list(in_degree)

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            in_degree_copy[v] -= 1
            if in_degree_copy[v] == 0:
                queue.append(v)

    tail_length = {i: p_min[i] for i in range(num_ops)}
    for u in reversed(topo_order):
        if adj[u]:
            tail_length[u] = p_min[u] + max(tail_length[v] for v in adj[u])

    machine_avail = defaultdict(lambda: defaultdict(int))
    op_end_time = {}
    schedule = {}

    ready_ops = [i for i in range(num_ops) if in_degree[i] == 0]

    while ready_ops:
        ready_ops.sort(key=lambda op: tail_length[op], reverse=True)
        u = ready_ops.pop(0)

        j_id = job_of[u]
        factory = job_factory[j_id]

        ready_time = max([op_end_time[p] for p in preds[u]], default=0)

        best_machine = None
        best_start = float('inf')
        best_end = float('inf')

        for k, p_uk in request_list[u].items():
            avail_k = machine_avail[factory][k]
            start_t = max(ready_time, avail_k)
            end_t = start_t + p_uk

            if end_t < best_end:
                best_end = end_t
                best_start = start_t
                best_machine = k

        schedule[u] = {
            'factory': factory,
            'machine': best_machine,
            'start': best_start,
            'duration': request_list[u][best_machine],
            'end': best_end
        }
        op_end_time[u] = best_end
        machine_avail[factory][best_machine] = best_end

        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                ready_ops.append(v)

    makespan = max(info['end'] for info in schedule.values()) if schedule else 0
    return makespan, schedule


def compute_bounds(num_ops, precedence_list, p_min, UB):
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    for u, v in precedence_list:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_ops) if in_degree[i] == 0])
    topo_order = []
    ES = {i: 0 for i in range(num_ops)}

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            ES[v] = max(ES[v], ES[u] + p_min[u])
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    LS = {i: UB - p_min[i] for i in range(num_ops)}
    for u in reversed(topo_order):
        for v in adj[u]:
            LS[u] = min(LS[u], LS[v] - p_min[u])

    return ES, LS


def create_var(num_ops, num_jobs, num_factories, request_list, job_of, E_star, ES, LS):
    s = {}
    x = {}
    f = {}
    m = {}
    xm = {}
    sf = {}
    sm = {}
    sfm = {}
    counter = 0

    # 1. Biến thời gian
    for i in range(num_ops):
        for t in range(ES[i], LS[i] + 1):
            counter += 1
            s[(i, t)] = counter
        for t in range(ES[i], LS[i] + 1):
            counter += 1
            x[(i, t)] = counter

    # 2. Biến nhà máy
    for j in range(num_jobs):
        max_q = min(j, num_factories - 1)
        for q in range(max_q + 1):
            counter += 1
            f[(j, q)] = counter

    # 3. Biến chọn máy
    for i in range(num_ops):
        for k in request_list[i].keys():
            counter += 1
            m[(i, k)] = counter
            counter += 1
            xm[(i, k)] = counter

    # 4. Biến cùng nhà máy
    for j1 in range(num_jobs):
        for j2 in range(j1 + 1, num_jobs):
            counter += 1
            sf[(j1, j2)] = counter

    # 5. Biến đè/trùng máy
    for i in range(num_ops):
        for j in range(i + 1, num_ops):
            if (i, j) not in E_star and (j, i) not in E_star:
                common_machines = set(request_list[i].keys()) & set(request_list[j].keys())
                for k in common_machines:
                    p_ik = request_list[i][k]
                    p_jk = request_list[j][k]
                    if not (ES[i] >= LS[j] + p_jk or ES[j] >= LS[i] + p_ik):
                        counter += 1
                        sm[(i, j, k)] = counter
                        if job_of[i] != job_of[j]:
                            counter += 1
                            sfm[(i, j, k)] = counter

    return s, x, f, m, xm, sf, sm, sfm, counter


def build_constraints(solver, num_ops, num_jobs, num_factories, precedence_list, request_list, job_of, E_star, ES, LS, first_ops, s, x, f, m, xm, sf, sm, sfm, args):
    cnf = CNF()

    # Exactly one factory per job
    for j in range(num_jobs):
        clauses = CardEnc.equals(lits=[f[(j, q)] for q in range(min(j, num_factories - 1) + 1)], bound=1, encoding=EncType.pairwise)
        cnf.extend(clauses.clauses)

    for i in range(num_ops):
        # Linking s and x order variables
        cnf.append([x[(i, ES[i])]])
        for t in range(ES[i], LS[i]):
            cnf.append([-x[(i, t + 1)], x[(i, t)]])
            cnf.append([-s[(i, t)], x[(i, t)]])
            cnf.append([-s[(i, t)], -x[(i, t + 1)]])
            cnf.append([-x[(i, t)], x[(i, t + 1)], s[(i, t)]])

        cnf.append([-s[(i, LS[i])], x[(i, LS[i])]])
        cnf.append([s[(i, LS[i])], -x[(i, LS[i])]])

        # Linking m and xm order variables
        request_machines = list(request_list[i].keys())
        cnf.append([xm[(i, request_machines[0])]])
        for idx in range(len(request_machines) - 1):
            machine = request_machines[idx]
            next_machine = request_machines[idx + 1]

            cnf.append([-xm[(i, next_machine)], xm[(i, machine)]])
            cnf.append([-m[(i, machine)], xm[(i, machine)]])
            cnf.append([-m[(i, machine)], -xm[(i, next_machine)]])
            cnf.append([-xm[(i, machine)], m[(i, machine)], xm[(i, next_machine)]])

        cnf.append([-m[(i, request_machines[-1])], xm[(i, request_machines[-1])]])
        cnf.append([m[(i, request_machines[-1])], -xm[(i, request_machines[-1])]])

    # Ràng buộc precedence (i -> j)
    for i, j in precedence_list:
        request_machines_i = list(request_list[i].keys())
        m_0 = request_machines_i[0]
        min_p = request_list[i][m_0]

        for t in range(ES[i], LS[i] + 1):
            finish_time = t + min_p
            if finish_time > LS[j]:
                cnf.append([-s[(i, t)]])
                continue
            elif finish_time > ES[j]:
                cnf.append([-s[(i, t)], x[(j, finish_time)]])

            pre_proc_time = min_p
            for idx in range(1, len(request_machines_i)):
                machine = request_machines_i[idx]
                proc_time = request_list[i][machine]

                if proc_time > pre_proc_time:
                    finish_time = t + proc_time

                    if finish_time > LS[j]:
                        cnf.append([-s[(i, t)], -xm[(i, machine)]])
                        break
                    elif finish_time > ES[j]:
                        cnf.append([-s[(i, t)], -xm[(i, machine)], x[(j, finish_time)]])

                    pre_proc_time = proc_time

    # Same factory constraints
    for j1 in range(num_jobs - 1):
        for j2 in range(j1 + 1, num_jobs):
            for q in range(min(j1, j2, num_factories - 1) + 1):
                cnf.append([-f[(j1, q)], -f[(j2, q)], sf[(j1, j2)]])
                cnf.append([-sf[(j1, j2)], -f[(j1, q)], f[(j2, q)]])
                cnf.append([-sf[(j1, j2)], -f[(j2, q)], f[(j1, q)]])

    # Overlap constraints
    for i in range(num_ops):
        for j in range(i + 1, num_ops):
            if (i, j) not in E_star and (j, i) not in E_star:
                common_machines = set(request_list[i].keys()) & set(request_list[j].keys())
                for k in common_machines:
                    p_ik = request_list[i][k]
                    p_jk = request_list[j][k]
                    if not (ES[i] >= LS[j] + p_jk or ES[j] >= LS[i] + p_ik):
                        cnf.append([-m[(i, k)], -m[(j, k)], sm[(i, j, k)]])
                        cnf.append([-sm[(i, j, k)], m[(i, k)]])
                        cnf.append([-sm[(i, j, k)], m[(j, k)]])
                        if job_of[i] != job_of[j]:
                            j1, j2 = min(job_of[i], job_of[j]), max(job_of[i], job_of[j])
                            cnf.append([-sm[(i, j, k)], -sf[(j1, j2)], sfm[(i, j, k)]])
                            cnf.append([-sfm[(i, j, k)], sm[(i, j, k)]])
                            cnf.append([-sfm[(i, j, k)], sf[(j1, j2)]])
                            same_lit = sfm[(i, j, k)]
                        else:
                            same_lit = sm[(i, j, k)]
                            print(f" Add overlap constraint for same job ops {i} and {j} on machine {k}")

                        for t in range(ES[i], LS[i] + 1):
                            clause = [-same_lit, -s[(i, t)]]

                            after_i = t + p_ik
                            before_i = t - p_jk
                            if after_i <= ES[j]:
                                continue
                            if before_i >= LS[j]:
                                continue
                            if after_i <= LS[j]:
                                clause.append(x[(j, after_i)])
                            if before_i >= ES[j]:
                                clause.append(-x[(j, before_i + 1)])
                            cnf.append(clause)

    # Ràng buộc bắc cầu E* (Xử lý tùy chọn --full_transitive và --half_transitive)
    if getattr(args, 'full_transitive', False) or getattr(args, 'half_transitive', False):
        for (u, v), w in E_star.items():
            if (u, v) not in precedence_list:
                if getattr(args, 'full_transitive', False) or u in first_ops:
                    for t in range(ES[u], LS[u] + 1):
                        finish_time = t + w
                        if finish_time > LS[v]:
                            cnf.append([-s[(u, t)]])
                        elif finish_time > ES[v]:
                            cnf.append([-s[(u, t)], x[(v, finish_time)]])

    # Symmetry Breaking (nếu được bật)
    if args.sb:
        for i in range(1, num_jobs):
            for factory in range(1, min(i + 1, num_factories)):
                if (i, factory) not in f:
                    continue

                clause = [-f[(i, factory)]]
                for j in range(factory - 1, i):
                    if (j, factory - 1) in f:
                        clause.append(f[(j, factory - 1)])

                cnf.append(clause)

    solver.append_formula(cnf)


def add_upper_bound_constraints(solver, last_ops, request_list, ES, LS, x, m, UB):
    for i in last_ops:
        for k, p_ik in request_list[i].items():
            latest_start = UB - p_ik
            if latest_start < ES[i]:
                solver.add_clause([-m[(i, k)]])
            elif latest_start < LS[i]:
                if (i, latest_start + 1) in x:
                    solver.add_clause([-m[(i, k)], -x[(i, latest_start + 1)]])


def solve_and_print(num_ops, num_jobs, num_factories, precedence_list, request_list, job_of, E_star, initial_UB, args):
    first_ops, last_ops = extract_data(num_ops, precedence_list)
    p_min = [min(req.values()) for req in request_list]
    current_UB = initial_UB
    best_schedule = None
    best_makespan = None

    ES, LS = compute_bounds(num_ops, precedence_list, p_min, current_UB)
    s, x, f, m, xm, sf, sm, sfm, _ = create_var(
        num_ops, num_jobs, num_factories, request_list, job_of, E_star, ES, LS
    )

    solver = Solver(name='cadical195')
    build_constraints(
        solver, num_ops, num_jobs, num_factories, precedence_list, request_list,
        job_of, E_star, ES, LS, first_ops, s, x, f, m, xm, sf, sm, sfm, args
    )
    while current_UB >= 0:
        print('------------------------------------------------------------------')
        print(f"[*] Trying with Upper Bound = {current_UB}...")

        add_upper_bound_constraints(solver, last_ops, request_list, ES, LS, x, m, current_UB)

        if not solver.solve():
            print("   UNSAT")
            break

        model = set(solver.get_model())
        schedule = {}
        for i in range(num_ops):
            assigned_machine = None
            for k in request_list[i].keys():
                if m[(i, k)] in model:
                    assigned_machine = k
                    break

            start_time = None
            for t in range(ES[i], LS[i] + 1):
                if s[(i, t)] in model:
                    start_time = t
                    break

            j_id = job_of[i]
            assigned_factory = None
            for q in range(num_factories):
                if (j_id, q) in f and f[(j_id, q)] in model:
                    assigned_factory = q
                    break

            duration = request_list[i][assigned_machine]
            schedule[i] = {
                'job': j_id,
                'factory': assigned_factory,
                'machine': assigned_machine,
                'start': start_time,
                'duration': duration,
                'end': start_time + duration
            }

        best_makespan = max(info['end'] for info in schedule.values())
        best_schedule = schedule
        print(f"  SAT ! Makespan = {best_makespan}")
        if verify_schedule(best_schedule, precedence_list, best_makespan):
            print(f"  Schedule is valid with Makespan = {best_makespan}")

        current_UB = best_makespan - 1

    if best_schedule is None:
        print("UNSAT).")
        return None, None

    print(f"\n Optimal Makespan = {best_makespan}\n")
    return best_makespan, best_schedule


def verify_schedule(schedule, precedence_list, C_max):
    if schedule is None:
        print("[Verify Failed] Empty schedule!")
        return False

    max_end = max(info['end'] for info in schedule.values())
    if max_end > C_max:
        print(f" [X] Lỗi Makespan: End time ({max_end}) is over C_max ({C_max})")
        return False

    for u, v in precedence_list:
        if schedule[u]['end'] > schedule[v]['start']:
            print(f" [X] Lỗi Precedence: Op {u} end at {schedule[u]['end']} but Op {v} starts at {schedule[v]['start']}")
            return False

    job_factories = defaultdict(set)
    for op, info in schedule.items():
        job_factories[info['job']].add(info['factory'])

    for j_id, factories in job_factories.items():
        if len(factories) > 1:
            print(f" [X] Lỗi Factory: Job {j_id} is assigned to multiple factories: {factories}")
            return False

    factory_machine_intervals = defaultdict(list)
    for op, info in schedule.items():
        key = (info['factory'], info['machine'])
        factory_machine_intervals[key].append((info['start'], info['end'], op))

    for (fac, mac), intervals in factory_machine_intervals.items():
        intervals.sort(key=lambda x: x[0])
        for idx in range(len(intervals) - 1):
            curr_start, curr_end, curr_op = intervals[idx]
            next_start, next_end, next_op = intervals[idx + 1]

            if curr_end > next_start:
                print(f" [X] Overlap: At Factory {fac}, Machine {mac}: Op {curr_op} [{curr_start}, {curr_end}) overlaps with Op {next_op} [{next_start}, {next_end})")
                return False
    return True


def main():
    parser = argparse.ArgumentParser(description="D-FJSSP SAT Solver")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to the data file")
    parser.add_argument("--factories", "-num_f", type=int, default=2, help="Number of factories (ignored if flexibilitydata is present)")
    parser.add_argument("--sb", action="store_true", help="Enable Symmetry Breaking")
    parser.add_argument("--half_transitive", action="store_true", help="Enable half transitive constraints E* (first op of each job only)")
    parser.add_argument("--full_transitive", action="store_true", help="Enable full transitive constraints E* (all new edges)")
    args = parser.parse_args()

    start_time = time.time()
    print(f"[*] Loading data from file: {args.input}")
    
    n_ops, n_machines, precedence_list, request_list, num_jobs, job_of, file_factories = load_data(args.input)

    if file_factories is not None:
        num_factories = file_factories
    else:
        num_factories = args.factories

    if args.full_transitive:
        transitive_mode = "FULL"
    elif args.half_transitive:
        transitive_mode = "HALF"
    else:
        transitive_mode = "OFF"

    print(f"[*] Running D-FJSSP SAT Solver with {num_factories} factories, Symmetry Breaking = {'ON' if args.sb else 'OFF'}, Transitive E* = {transitive_mode}")
    print("=" * 75)
    print(" D-FJSSP SAT SOLVER - PARALLEL FACTORIES SCHEDULING")
    print("=" * 75)

    print(f"  -> Operations: {n_ops} | Jobs: {num_jobs} | Machines: {n_machines} | Factories: {num_factories}")

    E_star = compute_E_star(n_ops, precedence_list, request_list)
    print("\n[*] Running Greedy Heuristic...")
    g_start = time.time()
    g_makespan, g_schedule = greedy_solve(
        num_ops=n_ops,
        num_machines=n_machines,
        num_factories=num_factories,
        precedence_list=precedence_list,
        request_list=request_list,
        job_of=job_of,
        num_jobs=num_jobs
    )
    g_time = time.time() - g_start
    print(f"  -> Greedy Solution: Makespan = {g_makespan} ({g_time:.4f}s)")

    print("\n[*] Initializing and solving the SAT model...")
    sat_start = time.time()
    best_makespan, best_schedule = solve_and_print(
        num_ops=n_ops,
        num_jobs=num_jobs,
        num_factories=num_factories,
        precedence_list=precedence_list,
        request_list=request_list,
        job_of=job_of,
        E_star=E_star,
        initial_UB=g_makespan,
        args=args
    )
    sat_time = time.time() - sat_start

    if best_schedule is not None:
        is_valid = verify_schedule(best_schedule, precedence_list, best_makespan)
        total_time = time.time() - start_time
        
        print(f" Summary:")
        print(f"  - Optimal Makespan   : {best_makespan}")
        print(f"  - Greedy Time        : {g_time:.4f}s")
        print(f"  - SAT Time           : {sat_time:.4f}s")
        print(f"  - Total Time         : {total_time:.4f}s")
        print(f"  - Schedule Status    : {'VALID' if is_valid else 'INVALID'}")
        print("=" * 75)


if __name__ == "__main__":
    main()