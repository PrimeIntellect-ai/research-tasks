# test_final_state.py
import os
import csv

def test_analyzer_go_exists():
    assert os.path.exists("/home/user/analyzer.go"), "The Go program /home/user/analyzer.go does not exist."
    assert os.path.isfile("/home/user/analyzer.go"), "/home/user/analyzer.go is not a file."

def test_database_exists():
    assert os.path.exists("/home/user/sales.db"), "The SQLite database /home/user/sales.db does not exist."

def test_report_csv_exists():
    assert os.path.exists("/home/user/report.csv"), "The output file /home/user/report.csv does not exist."
    assert os.path.isfile("/home/user/report.csv"), "/home/user/report.csv is not a file."

def test_report_csv_contents():
    expected_rows = [
        ["tx_id", "user_id", "amount", "timestamp", "moving_avg"],
        ["t06", "u2", "80.0", "2023-01-02T11:00:00Z", "50.00"],
        ["t07", "u2", "40.0", "2023-01-03T11:00:00Z", "46.67"],
        ["t08", "u2", "90.0", "2023-01-04T11:00:00Z", "70.00"],
        ["t09", "u3", "100.0", "2023-01-01T12:00:00Z", "100.00"],
        ["t11", "u3", "105.0", "2023-01-03T12:00:00Z", "73.33"]
    ]

    with open("/home/user/report.csv", "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in report.csv (including header), but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_go_module_initialized():
    assert os.path.exists("/home/user/go.mod"), "Go module was not initialized in /home/user (go.mod is missing)."