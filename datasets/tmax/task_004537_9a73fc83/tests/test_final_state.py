# test_final_state.py

import os
import pytest

def test_cleaner_c_and_executable_exist():
    c_file = "/home/user/cleaner.c"
    exe_file = "/home/user/cleaner"
    assert os.path.isfile(c_file), f"Source file not found: {c_file}"
    assert os.path.isfile(exe_file), f"Executable not found: {exe_file}"
    assert os.access(exe_file, os.X_OK), f"File is not executable: {exe_file}"

def test_error_log_content():
    log_file = "/home/user/error.log"
    assert os.path.isfile(log_file), f"Error log not found: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["2", "4", "6"]
    assert lines == expected_lines, f"Expected {expected_lines} in error.log, got {lines}"

def test_clean_data_csv_content():
    csv_file = "/home/user/clean_data.csv"
    assert os.path.isfile(csv_file), f"Output CSV not found: {csv_file}"

    with open(csv_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in {csv_file}, got {len(lines)}"

    # Check event IDs and approximate float values
    expected_data = {
        "1": 45.2,
        "3": 48.9,
        "5": 12.1
    }

    for line in lines:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid CSV format in line: '{line}'"
        event_id, sensor_val = parts

        assert event_id in expected_data, f"Unexpected event_id {event_id} in output"
        expected_val = expected_data[event_id]

        try:
            val_float = float(sensor_val)
        except ValueError:
            pytest.fail(f"Could not parse float from sensor_val: {sensor_val}")

        assert abs(val_float - expected_val) < 0.001, f"Expected sensor_val {expected_val} for event_id {event_id}, got {val_float}"