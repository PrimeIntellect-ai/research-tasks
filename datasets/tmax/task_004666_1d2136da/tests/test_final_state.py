# test_final_state.py
import os
import csv
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/process_sensors.cpp"), "C++ source file is missing."
    assert os.path.isfile("/home/user/process_sensors"), "Compiled binary is missing."
    assert os.path.isfile("/home/user/aggregated_sensors.csv"), "Aggregated CSV output is missing."
    assert os.path.isfile("/home/user/pipeline.log"), "Pipeline log file is missing."

def test_aggregated_csv_content():
    csv_path = "/home/user/aggregated_sensors.csv"
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Aggregated CSV is empty."

    header = rows[0]
    expected_header = ["bucket_start_ts", "sensor_id", "avg_temp", "avg_humidity"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    data_rows = rows[1:]
    expected_data = [
        ["1600000000000", "A", "22.00", "52.00"],
        ["1600000000000", "B", "12.00", "42.00"],
        ["1600000900000", "A", "27.00", "57.00"],
        ["1600000900000", "B", "17.00", "46.50"]
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data_rows)}"

    for i, expected_row in enumerate(expected_data):
        assert data_rows[i] == expected_row, f"Row {i+1} mismatch. Expected {expected_row}, got {data_rows[i]}"

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, "Pipeline log should contain at least 3 lines."

    expected_warnings = [
        "[WARN] Dropped row with timestamp 1600001200000 due to out-of-bounds temperature.",
        "[WARN] Dropped row with timestamp 1600000500000 due to out-of-bounds temperature."
    ]

    for warn in expected_warnings:
        assert warn in lines, f"Expected warning '{warn}' not found in log."

    assert lines[-1] == "[INFO] Pipeline finished.", "The last line of the log must be the finished info message."