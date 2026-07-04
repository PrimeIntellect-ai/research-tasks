# test_final_state.py
import os
import csv
import socket
import pytest

def test_mongodb_directory_exists():
    db_path = "/home/user/mongodb_data"
    assert os.path.isdir(db_path), f"MongoDB data directory {db_path} does not exist."

def test_mongodb_port_open():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex(('127.0.0.1', 27017))
        assert result == 0, "MongoDB is not listening on port 27017."
    finally:
        s.close()

def test_analyze_script_exists():
    script_path = "/home/user/analyze_deadlocks.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_csv_report_contents():
    csv_path = "/home/user/deadlock_report.csv"
    assert os.path.isfile(csv_path), f"CSV report {csv_path} does not exist."

    expected_rows = [
        ["sequence_order", "tx_id", "waits_for", "operation"],
        ["1", "TX-42", "TX-88", "lock_table_users"],
        ["2", "TX-88", "TX-12", "lock_table_billing"],
        ["3", "TX-12", "TX-42", "lock_table_logs"]
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} in CSV does not match expected. Got {actual}, expected {expected}."