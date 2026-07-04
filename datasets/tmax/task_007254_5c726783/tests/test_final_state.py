# test_final_state.py
import os
import csv
import json
import stat
import pytest

SCRIPT_PATH = "/home/user/analyze_backups.sh"
REPORT_PATH = "/home/user/report.csv"
BACKUPS_PATH = "/home/user/backups.json"
GRAPH_PATH = "/home/user/replication_graph.csv"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_report_content():
    assert os.path.isfile(REPORT_PATH), f"Report {REPORT_PATH} does not exist."
    assert os.path.isfile(BACKUPS_PATH), f"Data file {BACKUPS_PATH} is missing."
    assert os.path.isfile(GRAPH_PATH), f"Data file {GRAPH_PATH} is missing."

    # Read backups
    with open(BACKUPS_PATH, "r") as f:
        backups = json.load(f)

    backup_info = {}
    for b in backups:
        backup_info[b["db_instance"]] = {
            "status": b["status"],
            "size_gb": b["size_gb"]
        }

    # Read replication graph
    primary_to_replicas = {}
    with open(GRAPH_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["primary"].strip()
            r = row["replica"].strip()
            if p not in primary_to_replicas:
                primary_to_replicas[p] = []
            primary_to_replicas[p].append(r)

    # Calculate expected report
    expected_rows = []
    for primary, replicas in primary_to_replicas.items():
        # Check if at least one replica failed
        has_failed_replica = any(
            backup_info.get(r, {}).get("status") == "failed" for r in replicas
        )

        if has_failed_replica:
            num_replicas = len(replicas)

            # Calculate total size of successful backups for cluster
            total_size = 0

            # Primary size
            if backup_info.get(primary, {}).get("status") == "success":
                total_size += backup_info[primary]["size_gb"]

            # Replicas size
            for r in replicas:
                if backup_info.get(r, {}).get("status") == "success":
                    total_size += backup_info[r]["size_gb"]

            expected_rows.append(f"{primary},{num_replicas},{total_size}")

    expected_rows.sort()
    expected_content = "\n".join(expected_rows)

    # Read actual report
    with open(REPORT_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    actual_content = "\n".join(actual_lines)

    assert actual_content == expected_content, (
        f"Report content in {REPORT_PATH} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )