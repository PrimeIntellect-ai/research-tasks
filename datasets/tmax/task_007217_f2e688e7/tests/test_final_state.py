# test_final_state.py

import os
import csv
from collections import defaultdict

WORKSPACE_DIR = "/home/user/workspace"
RAW_METRICS_FILE = os.path.join(WORKSPACE_DIR, "raw_metrics.csv")
SUMMARY_FILE = os.path.join(WORKSPACE_DIR, "summary.csv")

SCRIPTS = [
    "1_filter.sh",
    "2_impute.sh",
    "3_aggregate.sh",
    "run_pipeline.sh"
]

def test_scripts_exist_and_executable():
    """Verify that all required scripts exist and are executable."""
    for script in SCRIPTS:
        script_path = os.path.join(WORKSPACE_DIR, script)
        assert os.path.isfile(script_path), f"Missing script: {script_path} does not exist."
        assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_summary_file_exists():
    """Verify that the final output file summary.csv exists."""
    assert os.path.isfile(SUMMARY_FILE), f"Missing output file: {SUMMARY_FILE} does not exist."

def compute_expected_summary():
    """Derive the expected summary.csv contents from raw_metrics.csv."""
    assert os.path.isfile(RAW_METRICS_FILE), "raw_metrics.csv missing, cannot compute expected state."

    valid_statuses = {"200", "301", "404", "500"}

    # server_id -> list of (cpu, mem)
    server_data = defaultdict(list)
    last_known = {} # server_id -> (cpu, mem)

    with open(RAW_METRICS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status_code"] not in valid_statuses:
                continue

            server_id = row["server_id"]
            cpu_raw = row["cpu_usage"]
            mem_raw = row["mem_usage"]

            # Imputation
            if cpu_raw == "-":
                cpu = last_known[server_id]["cpu"]
            else:
                cpu = float(cpu_raw)

            if mem_raw == "-":
                mem = last_known[server_id]["mem"]
            else:
                mem = float(mem_raw)

            last_known[server_id] = {"cpu": cpu, "mem": mem}
            server_data[server_id].append((cpu, mem))

    expected = []
    for server_id in sorted(server_data.keys()):
        cpus = [x[0] for x in server_data[server_id]]
        mems = [x[1] for x in server_data[server_id]]

        avg_cpu = sum(cpus) / len(cpus)
        avg_mem = sum(mems) / len(mems)

        expected.append(f"{server_id},{avg_cpu:.2f},{avg_mem:.2f}")

    return expected

def test_summary_content():
    """Verify that summary.csv contains the correctly filtered, imputed, and aggregated data."""
    expected_lines = compute_expected_summary()

    with open(SUMMARY_FILE, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} rows in summary.csv, found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Row {i+1} mismatch in summary.csv.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )