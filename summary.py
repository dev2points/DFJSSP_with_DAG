#!/usr/bin/env python3

import argparse
import csv
import os
import re

# ============================================================
# Time checkpoints
# ============================================================

TIME_LIMITS = [600, 1800]


# ============================================================
# Parse one log file
# ============================================================


def parse_log(filepath):
    """Parse one 3600s SAT solver log."""

    try:
        with open(
            filepath, "r", encoding="utf-8", errors="ignore"
        ) as f:
            text = f.read()

    except Exception as e:
        print(f"[!] Cannot read {filepath}: {e}")
        return None

    # ========================================================
    # 1. Instance name
    # ========================================================

    m = re.search(r"Loading data from file:\s*(.+)", text)

    if m:
        data_path = m.group(1).strip()
        name = os.path.basename(data_path.rstrip("/\\"))
    else:
        name = os.path.splitext(os.path.basename(filepath))[0]

    # ========================================================
    # 2. Initial Upper Bound
    # ========================================================

    m = re.search(r"Greedy Solution:\s*Makespan\s*=\s*(\d+)", text)
    upper_bound = int(m.group(1)) if m else None

    # ========================================================
    # 3. SAT events
    # ========================================================

    sat_pattern = re.compile(
        r"SAT\s*!\s*Makespan\s*=\s*(\d+)"
        r".*?"
        r"Total time:\s*([\d.]+)\s*seconds",
        re.DOTALL,
    )

    sat_events = []
    for m in sat_pattern.finditer(text):
        makespan = int(m.group(1))
        time = float(m.group(2))
        sat_events.append({"time": time, "makespan": makespan})

    # ========================================================
    # 4. Check whether UNSAT exists
    # ========================================================

    unsat_exists = bool(re.search(r"\bUNSAT\b", text, re.IGNORECASE))

    # ========================================================
    # 5. Summary: SAT Time
    # ========================================================

    m = re.search(r"-\s*SAT\s+Time\s*:\s*([\d.]+)\s*s", text, re.IGNORECASE)
    sat_time = float(m.group(1)) if m else None

    # ========================================================
    # 6. Summary: Total Time
    # ========================================================

    m = re.search(r"-\s*Total\s+Time\s*:\s*([\d.]+)\s*s", text, re.IGNORECASE)
    summary_total_time = float(m.group(1)) if m else None

    # ========================================================
    # 7. runlim real time & runlim status
    # ========================================================

    m = re.search(r"\[runlim\]\s+real:\s*([\d.]+)\s*seconds", text)
    if m:
        total_time = float(m.group(1))
    elif summary_total_time is not None:
        total_time = summary_total_time
    else:
        m = re.search(r"\[runlim\]\s+time:\s*([\d.]+)\s*seconds", text)
        total_time = float(m.group(1)) if m else None

    # Bổ sung trích xuất [runlim] status
    m_runlim_status = re.search(r"\[runlim\]\s+status:\s*(.+)", text)
    if m_runlim_status:
        runlim_status_str = m_runlim_status.group(1).strip().lower()
        if "out of time" in runlim_status_str:
            fallback_status = "TO"
        else:
            fallback_status = "MO"
    else:
        fallback_status = "undefined"

    # ========================================================
    # 8. Optimal Makespan from summary
    # ========================================================

    m = re.search(r"Optimal\s+Makespan\s*=\s*(\d+)", text, re.IGNORECASE)
    optimal_makespan = int(m.group(1)) if m else None

    # ========================================================
    # 9. Result
    # ========================================================

    result = {
        "name": name,
        "upper bound": upper_bound,
        "optimal makespan": optimal_makespan,
        "SAT time": sat_time,
        "total time": total_time,
    }

    # ========================================================
    # 10. Analyze each checkpoint
    # ========================================================

    for limit in TIME_LIMITS:
        events = [event for event in sat_events if event["time"] <= limit]

        if events:
            best_event = min(events, key=lambda x: x["makespan"])
            best_makespan = best_event["makespan"]
            best_time = best_event["time"]
        else:
            best_makespan = None
            best_time = None

        opt_proved = (
            unsat_exists
            and sat_time is not None
            and sat_time <= limit
            and best_makespan is not None
        )

        # ----------------------------------------------------
        # Status determination logic
        # ----------------------------------------------------
        if opt_proved:
            status = "OPT"
        else:
            status = fallback_status

        # ----------------------------------------------------
        # Add * for OPT
        # ----------------------------------------------------
        if status == "OPT" and best_makespan is not None:
            displayed_makespan = f"{best_makespan}*"
        else:
            displayed_makespan = best_makespan

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------
        result[f"{limit}s best makespan"] = displayed_makespan
        result[f"{limit}s found at"] = best_time
        result[f"{limit}s status"] = status
        result[f"{limit}s optimal proved at"] = (
            sat_time if opt_proved else None
        )

    return result


# ============================================================
# Collect logs recursively
# ============================================================


def collect_logs(root_dir):
    results = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if not filename.lower().endswith((".log", ".txt")):
                continue

            filepath = os.path.join(root, filename)
            print(f"[+] Processing: {filepath}")

            result = parse_log(filepath)
            if result is not None:
                results.append(result)

    return results


# ============================================================
# Save CSV
# ============================================================


def save_csv(results, output_file):
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fieldnames = [
        "name",
        "upper bound",
        "600s best makespan",
        "600s found at",
        "600s status",
        "600s optimal proved at",
        "1800s best makespan",
        "1800s found at",
        "1800s status",
        "1800s optimal proved at",
        "optimal makespan",
        "SAT time",
        "total time",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


# ============================================================
# Print statistics
# ============================================================


def print_statistics(results):
    print()
    print("=" * 80)
    print("STATISTICS")
    print("=" * 80)

    print(f"Total instances: {len(results)}\n")

    for limit in TIME_LIMITS:
        opt = sum(1 for r in results if r[f"{limit}s status"] == "OPT")
        to = sum(1 for r in results if r[f"{limit}s status"] == "TO")
        mo = sum(1 for r in results if r[f"{limit}s status"] == "MO")
        undefined = sum(
            1 for r in results if r[f"{limit}s status"] == "undefined"
        )

        print(f"[{limit}s]")
        print(f"  OPT        : {opt}")
        print(f"  TO         : {to}")
        print(f"  MO         : {mo}")
        print(f"  UNDEFINED  : {undefined}")
        print()


# ============================================================
# Main
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Parse 1800s SAT solver logs and "
            "extract results at 600s, 1800s. "
        )
    )

    parser.add_argument("input_dir", help="Root directory containing log files")

    parser.add_argument(
        "output_csv",
        nargs="?",
        default="summary/results.csv",
        help="Output CSV filename (mặc định: summary/results.csv)",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"[!] Directory does not exist: {args.input_dir}")
        return

    results = collect_logs(args.input_dir)
    results.sort(key=lambda x: x["name"])

    save_csv(results, args.output_csv)
    print_statistics(results)

    print("=" * 80)
    print(f"[*] Processed files : {len(results)}")
    print(f"[*] Output CSV      : {args.output_csv}")
    print("=" * 80)


if __name__ == "__main__":
    main()