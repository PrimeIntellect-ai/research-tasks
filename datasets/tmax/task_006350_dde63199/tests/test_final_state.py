# test_final_state.py

import os
import csv

def test_clean_sensors_csv_exists_and_correct():
    file_path = '/home/user/clean_sensors.csv'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_rows = [
        ["tx_id", "timestamp_ms", "sensor_type", "normalized_value"],
        ["tx01", "1625000001", "TEMP", "25.00"],
        ["tx03", "1625001500", "PRESSURE", "68.95"],
        ["tx07", "1625005000", "TEMP", "20.00"]
    ]

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, (
        f"Contents of {file_path} do not match expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )

def test_pipeline_log_exists_and_correct():
    log_path = '/home/user/pipeline.log'
    assert os.path.exists(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_log = "[INFO] Processed 3 valid rows, dropped 2 duplicates, dropped 2 malformed."

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    # Ignore empty lines at the end
    actual_lines = [line for line in lines if line.strip()]

    assert len(actual_lines) == 1, (
        f"Expected exactly one non-empty line in {log_path}, "
        f"but found {len(actual_lines)}."
    )

    assert actual_lines[0] == expected_log, (
        f"Log file content does not match expected format.\n"
        f"Expected: {expected_log}\n"
        f"Actual: {actual_lines[0]}"
    )