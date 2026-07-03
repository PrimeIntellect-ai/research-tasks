# test_final_state.py
import os
import csv
import pytest

def test_go_program_exists():
    assert os.path.exists("/home/user/process_metrics.go"), "Go program /home/user/process_metrics.go is missing"
    assert os.path.isfile("/home/user/process_metrics.go"), "/home/user/process_metrics.go is not a file"

def test_valid_metrics_csv():
    valid_csv_path = "/home/user/valid_metrics.csv"
    assert os.path.exists(valid_csv_path), f"Output file missing: {valid_csv_path}"

    with open(valid_csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "valid_metrics.csv is empty"
    assert reader[0] == ["timestamp", "server_id", "cpu_pct", "ram_mb", "event_details"], "Incorrect header in valid_metrics.csv"

    expected_rows = [
        ["2023-10-12T10:00:00Z", "srv-1", "45.5", "2048", "Normal operation"],
        ["2023-10-12T10:01:00Z", "srv-2", "99.9", "4096", "High load detected\nInvestigate immediately"],
        ["2023-10-12T10:04:00Z", "srv-1", "22.1", "8192", "Routine backup started\nLines: 400\nStatus: OK"],
        ["2023-10-12T10:05:00Z", "srv-2", "50.0", "4096", "Normal operation"],
        ["2023-10-12T10:07:00Z", "srv-1", "10.0", "2048", "Idle"],
        ["2023-10-12T10:08:00Z", "srv-2", "15.5", "4096", "Idle"],
        ["2023-10-12T10:09:00Z", "srv-3", "18.0", "1024", "Idle"],
    ]

    assert len(reader) - 1 == len(expected_rows), f"Expected {len(expected_rows)} valid rows, but found {len(reader) - 1}"

    for i, expected_row in enumerate(expected_rows, start=1):
        assert reader[i] == expected_row, f"Row {i} in valid_metrics.csv does not match expected output."

def test_invalid_metrics_csv():
    invalid_csv_path = "/home/user/invalid_metrics.csv"
    assert os.path.exists(invalid_csv_path), f"Output file missing: {invalid_csv_path}"

    with open(invalid_csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "invalid_metrics.csv is empty"
    assert reader[0] == ["timestamp", "server_id", "cpu_pct", "ram_mb", "event_details"], "Incorrect header in invalid_metrics.csv"

    expected_rows = [
        ["2023-10-12 10:02:00", "srv-1", "105.0", "2048", "Invalid CPU spike"],
        ["2023-10-12T10:03:00Z", "srv-3", "12.0", "-500", "Invalid RAM allocation"],
        ["2023-10-12 10:06:00", "srv-3", "NaN", "1024", "Broken float"],
    ]

    assert len(reader) - 1 == len(expected_rows), f"Expected {len(expected_rows)} invalid rows, but found {len(reader) - 1}"

    for i, expected_row in enumerate(expected_rows, start=1):
        assert reader[i] == expected_row, f"Row {i} in invalid_metrics.csv does not match expected output."