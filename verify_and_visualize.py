import argparse
import ast
import os
from pathlib import Path
import re
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

def extract_last_schedule(log_file_path):
    """Read the log file and extract the last schedule."""
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Cannot find log file at: {log_file_path}")

    with open(log_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    schedule_matches = re.findall(r"Schedule:\s*(\{.*\})", content)

    if not schedule_matches:
        raise ValueError(f"Cannot find a valid schedule in {log_file_path}")

    return ast.literal_eval(schedule_matches[-1])


def verify_schedule_independent(schedule, dataset_path=None):
    
    errors = []
    if not schedule:
        return False, ["Schedule empty!"], 0

    for op_id, info in schedule.items():
        if info["start"] + info["duration"] != info["end"]:
            errors.append(
                f"[Time logic] Op {op_id}: start ({info['start']}) + duration ({info['duration']}) != end ({info['end']})"
            )

    if dataset_path:
        if not os.path.exists(dataset_path):
            errors.append(
                f"[Dataset]  Cannot find dataset file: {dataset_path}"
            )
        else:
            try:
                (
                    n_ops,
                    n_mac,
                    prec,
                    request_list,
                    n_jobs,
                    job_of,
                    num_factories,
                ) = load_data(dataset_path)

                for op_id, info in schedule.items():
                    if op_id < 0 or op_id >= len(request_list):
                        errors.append(
                                f"[Error Dataset] Op {op_id} trong schedule vượt quá số lượng operation của Dataset (max: {len(request_list)-1})"
                            )
                        continue

                    valid_machine_map = request_list[op_id]
                    assigned_machine = info["machine"]
                    assigned_duration = info["duration"]

                    if assigned_machine not in valid_machine_map:
                        errors.append(
                            f"[Error Machine] Op {op_id} is assigned to Machine {assigned_machine}, "
                            f"but the list of valid machines in the Dataset only includes: {list(valid_machine_map.keys())}"
                        )
                    else:
                        expected_duration = valid_machine_map[assigned_machine]
                        if assigned_duration != expected_duration:
                            errors.append(
                                f"[Error Duration] Op {op_id} run on Machine {assigned_machine}  duration = {assigned_duration}, "
                                f"but Dataset defines duration = {expected_duration}"
                            )

                    if op_id in job_of and info["job"] != job_of[op_id]:
                        errors.append(
                            f"[Error Job ID] Op {op_id} of Job {info['job']} in schedule, "
                            f"but Dataset defines it as Job {job_of[op_id]}"
                        )

            except Exception as e:
                errors.append(f"[Dataset] Error reading file dataset: {str(e)}")

    job_factories = defaultdict(set)
    for op_id, info in schedule.items():
        job_factories[info["job"]].add(info["factory"])

    for j_id, factories in job_factories.items():
        if len(factories) > 1:
            errors.append(
                f"[Factory] Job {j_id} in multiple factories: {factories}"
            )

    machine_tasks = defaultdict(list)
    for op_id, info in schedule.items():
        machine_tasks[(info["factory"], info["machine"])].append(
            (info["start"], info["end"], op_id)
        )

    for (fac, mac), tasks in machine_tasks.items():
        tasks.sort(key=lambda x: x[0])  # Sắp xếp theo thời gian bắt đầu
        for i in range(len(tasks) - 1):
            if tasks[i][1] > tasks[i + 1][0]:
                errors.append(
                    f"[Overlapping] Fac {fac}, Mac {mac}: Op {tasks[i][2]} (end: {tasks[i][1]}) "
                    f"overlaps with Op {tasks[i+1][2]} (start: {tasks[i+1][0]})"
                )

    job_ops = defaultdict(list)
    for op_id, info in schedule.items():
        job_ops[info["job"]].append((op_id, info["start"], info["end"]))

    for j_id, ops in job_ops.items():
        ops.sort(key=lambda x: x[0])  
        for i in range(len(ops) - 1):
            if ops[i][2] > ops[i + 1][1]:
                errors.append(
                    f"[Precedence] Job {j_id}: Op {ops[i][0]} (end: {ops[i][2]}) "
                    f"don't finish before Op {ops[i+1][0]} (start: {ops[i+1][1]}) starts"
                )

    makespan = max(info["end"] for info in schedule.values())
    return len(errors) == 0, errors, makespan


def visualize_gantt_with_table(
    schedule, makespan, output_path="schedule_gantt_with_table.png"
):
    num_ops = len(schedule)
    num_machines = len(
        set((info["factory"], info["machine"]) for info in schedule.values())
    )

    gantt_height = max(5, num_machines * 0.6)
    table_height = max(4, num_ops * 0.45)
    total_height = gantt_height + table_height

    fig, (ax_gantt, ax_table) = plt.subplots(
        2,
        1,
        figsize=(16, total_height),
        gridspec_kw={"height_ratios": [gantt_height, table_height]},
    )

    factory_machines = sorted(
        list(set((info["factory"], info["machine"]) for info in schedule.values()))
    )
    y_labels = [f"Fac {fac} - Mac {mac}" for fac, mac in factory_machines]
    y_positions = {fm: i for i, fm in enumerate(factory_machines)}

    unique_jobs = sorted(list(set(info["job"] for info in schedule.values())))
    cmap = plt.get_cmap("tab10", len(unique_jobs))
    job_colors = {j: cmap(i) for i, j in enumerate(unique_jobs)}

    for op_id, info in schedule.items():
        fm = (info["factory"], info["machine"])
        y_pos = y_positions[fm]
        start = info["start"]
        duration = info["duration"]
        job_id = info["job"]
        color = job_colors[job_id]

        ax_gantt.barh(
            y_pos,
            duration,
            left=start,
            height=0.6,
            align="center",
            color=color,
            edgecolor="black",
            linewidth=0.8,
            alpha=0.85,
        )

        ax_gantt.text(
            start + duration / 2,
            y_pos,
            f"O{op_id} (J{job_id})",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=8,
        )

    for i in range(len(factory_machines) - 1):
        curr_fac = factory_machines[i][0]
        next_fac = factory_machines[i + 1][0]
        if curr_fac != next_fac:
            ax_gantt.axhline(
                y=i + 0.5,
                color="gray",
                linestyle="--",
                linewidth=1.5,
                alpha=0.7,
            )

    ax_gantt.set_yticks(range(len(factory_machines)))
    ax_gantt.set_yticklabels(y_labels, fontsize=9)
    ax_gantt.set_xlabel("Time", fontsize=11, fontweight="bold")
    ax_gantt.set_title(
        f"Makespan = {makespan}", fontsize=13, fontweight="bold"
    )
    ax_gantt.grid(axis="x", linestyle="--", alpha=0.6)

    ax_table.axis("tight")
    ax_table.axis("off")

    table_data = [[
        "Operation ID",
        "Job ID",
        "Factory",
        "Machine",
        "Start Time",
        "Duration",
        "End Time",
    ]]
    sorted_ops = sorted(schedule.items(), key=lambda x: x[0])
    for op_id, info in sorted_ops:
        table_data.append([
            f"Op {op_id}",
            f"Job {info['job']}",
            f"Factory {info['factory']}",
            f"Machine {info['machine']}",
            str(info["start"]),
            str(info["duration"]),
            str(info["end"]),
        ])

    table = ax_table.table(
        cellText=table_data, loc="center", cellLoc="center", colWidths=[0.14] * 7
    )
    table.auto_set_font_size(False)

    # TỰ ĐỘNG TÍNH FONT SIZE THEO SỐ DÒNG BẢNG ĐỂ TRÁNH TRÀN CHỮ
    font_size = max(6, min(10, 120 / num_ops))
    table.set_fontsize(font_size)

    # SCALE HÀNG CỦA BẢNG
    table.scale(1.0, 1.2)

    # Formatting Header
    for i in range(7):
        table[(0, i)].get_text().set_fontweight("bold")
        table[(0, i)].set_facecolor("#404040")
        table[(0, i)].get_text().set_color("white")

    # Formatting dòng dữ liệu theo màu đại diện của từng Job
    for row_idx, (op_id, info) in enumerate(sorted_ops, start=1):
        job_id = info["job"]
        c = job_colors[job_id]
        for col_idx in range(7):
            table[(row_idx, col_idx)].set_facecolor((*c[:3], 0.2))


    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"[+] Generated visualization: {output_path}")


def resolve_paths(input_path_str):
    
    input_path = Path(input_path_str)
    parts = list(input_path.parts)  # Chuyển các thư mục thành danh sách
    stem_name = input_path.stem  # Tên file bỏ đuôi (vd: mfjs01)

    dataset_path = None
    if "fmj" in parts:
        dataset_path = os.path.join("datasets", "fmj", stem_name)
    elif "brandimarte" in parts:
        dataset_path = os.path.join("datasets", "brandimarte", stem_name)
    elif "rdata" in parts:
        dataset_path = os.path.join("datasets", "rdata", f"{stem_name}.txt")
    else:
        dataset_path = os.path.join("datasets", stem_name)

    if parts and parts[0] == "results":
        parts[0] = "visualize"
    else:
        parts.insert(0, "visualize")

    output_path = Path(*parts).with_suffix(".png")

    return str(dataset_path), str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Verify schedule from log and visualize Gantt chart with table."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="results/4factories/fmj/mfjs01.log",
        help="File path of log to verify and visualize (default: results/4factories/fmj/mfjs01.log)",
    )
    parser.add_argument(
        "--dataset",
        "-d",
        type=str,
        default=None,
        help="File path of dataset to verify against (default: auto-determined based on input log path)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="File path to save the output PNG (default: auto-determined based on input log path)",
    )
    args = parser.parse_args()

    auto_dataset_path, auto_output_path = resolve_paths(args.input)

    dataset_path = args.dataset if args.dataset else auto_dataset_path
    output_path = args.output if args.output else auto_output_path

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"[*] Input Log : {args.input}")
    print(f"[*] Dataset   : {dataset_path}")
    print(f"[*] Output PNG: {output_path}")

    try:
        schedule = extract_last_schedule(args.input)
    except Exception as e:
        print(f"Error extracting schedule: {e}")
        return

    is_valid, errors, makespan = verify_schedule_independent(
        schedule, dataset_path=dataset_path
    )

    if is_valid:
        print(f" SUCCESS! Schedule is valid. Makespan = {makespan}")
        visualize_gantt_with_table(schedule, makespan, output_path=output_path)
    else:
        print(" FAILED! Schedule is invalid:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    main()