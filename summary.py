
#!/usr/bin/env python3

import os
import re
import csv
import argparse


def parse_log(filepath):
    """Parse một file log của SAT solver."""

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        print(f"[!] Cannot read {filepath}: {e}")
        return None

    # ------------------------------------------------------------
    # 1. Instance name
    # ------------------------------------------------------------
    m = re.search(
        r"Loading data from file:\s*(.+)",
        text
    )

    if m:
        data_path = m.group(1).strip()
        name = os.path.basename(data_path.rstrip("/\\"))
    else:
        name = os.path.splitext(os.path.basename(filepath))[0]

    # ------------------------------------------------------------
    # 2. Initial Upper Bound
    # ------------------------------------------------------------
    m = re.search(
        r"Greedy Solution:\s*Makespan\s*=\s*(\d+)",
        text
    )

    upper_bound = int(m.group(1)) if m else None

    # ------------------------------------------------------------
    # 3. Best Makespan
    # ------------------------------------------------------------
    sat_makespans = [
        int(x)
        for x in re.findall(
            r"SAT\s*!\s*Makespan\s*=\s*(\d+)",
            text
        )
    ]

    best_makespan = (
        min(sat_makespans)
        if sat_makespans
        else None
    )

    # ------------------------------------------------------------
    # 4. Status
    # ------------------------------------------------------------

    # Timeout
    timeout = bool(
        re.search(
            r"\[runlim\]\s+status:\s*out of time",
            text,
            re.IGNORECASE
        )
    )

    # UNSAT
    unsat_exists = bool(
        re.search(
            r"\bUNSAT\b",
            text,
            re.IGNORECASE
        )
    )

    if timeout:
        status = "TO"

    elif unsat_exists and best_makespan is not None:
        status = "OPT"

    else:
        status = "MO"

    # ------------------------------------------------------------
    # 5. Total time
    # ------------------------------------------------------------
    m = re.search(
        r"\[runlim\]\s+real:\s*([\d.]+)\s*seconds",
        text
    )

    if m:
        total_time = float(m.group(1))
    else:
        m = re.search(
            r"\[runlim\]\s+time:\s*([\d.]+)\s*seconds",
            text
        )

        total_time = (
            float(m.group(1))
            if m
            else None
        )

    return {
        "name": name,
        "upper bound": upper_bound,
        "best makespan": best_makespan,
        "status": status,
        "total time": total_time,
    }


def collect_logs(root_dir):
    """Duyệt đệ quy toàn bộ thư mục."""

    results = []

    for root, dirs, files in os.walk(root_dir):

        for filename in files:

            if not filename.lower().endswith(
                (".log", ".txt")
            ):
                continue

            filepath = os.path.join(
                root,
                filename
            )

            print(f"[+] Processing: {filepath}")

            result = parse_log(filepath)

            if result is not None:
                results.append(result)

    return results


def save_csv(results, output_file):

    fieldnames = [
        "name",
        "upper bound",
        "best makespan",
        "status",
        "total time",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Recursively parse SAT solver logs "
            "and export results to CSV."
        )
    )

    # ------------------------------------------------------------
    # Input directory
    # ------------------------------------------------------------
    parser.add_argument(
        "input_dir",
        help="Root directory containing log files"
    )

    # ------------------------------------------------------------
    # Output CSV
    # ------------------------------------------------------------
    parser.add_argument(
        "output_csv",
        help="Output CSV filename"
    )

    args = parser.parse_args()

    # ------------------------------------------------------------
    # Validate input directory
    # ------------------------------------------------------------
    if not os.path.isdir(args.input_dir):

        print(
            f"[!] Directory does not exist: "
            f"{args.input_dir}"
        )

        return

    # ------------------------------------------------------------
    # Collect
    # ------------------------------------------------------------
    results = collect_logs(
        args.input_dir
    )

    # ------------------------------------------------------------
    # Sort by instance name
    # ------------------------------------------------------------
    results.sort(
        key=lambda x: x["name"]
    )

    # ------------------------------------------------------------
    # Save
    # ------------------------------------------------------------
    save_csv(
        results,
        args.output_csv
    )

    print()
    print("=" * 70)
    print(
        f"[*] Processed files : {len(results)}"
    )
    print(
        f"[*] Output CSV      : {args.output_csv}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()

