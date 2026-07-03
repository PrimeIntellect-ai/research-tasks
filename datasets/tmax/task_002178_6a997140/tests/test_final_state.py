# test_final_state.py

import os
import csv
import pytest

CSV_PATH = '/home/user/output.csv'
C_SOURCE_PATH = '/home/user/analyze.c'
C_BIN_PATH = '/home/user/analyze'

EXPECTED_ROWS = [
    ['device_name', 'timestamp', 'temperature', 'moving_avg'],
    ['Alpha_Sensor', '2023-10-01 10:00:00', '20.0', '20.00'],
    ['Alpha_Sensor', '2023-10-01 10:05:00', '22.0', '21.00'],
    ['Alpha_Sensor', '2023-10-01 10:10:00', '24.0', '22.00'],
    ['Alpha_Sensor', '2023-10-01 10:15:00', '26.0', '24.00'],
    ['Beta_Sensor', '2023-10-01 10:00:00', '15.0', '15.00'],
    ['Beta_Sensor', '2023-10-01 10:05:00', '16.0', '15.50'],
    ['Beta_Sensor', '2023-10-01 10:10:00', '18.0', '16.33']
]

def test_c_program_exists():
    assert os.path.exists(C_SOURCE_PATH), f"C source file not found at {C_SOURCE_PATH}"
    assert os.path.exists(C_BIN_PATH), f"Compiled C binary not found at {C_BIN_PATH}"
    assert os.access(C_BIN_PATH, os.X_OK), f"Binary at {C_BIN_PATH} is not executable"

def test_output_csv_exists():
    assert os.path.exists(CSV_PATH), f"Output CSV file not found at {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"Path {CSV_PATH} is not a file"

def test_output_csv_content():
    assert os.path.exists(CSV_PATH), "Cannot check content because CSV file is missing."

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, "The CSV file is empty."

    # Check header
    assert actual_rows[0] == EXPECTED_ROWS[0], f"CSV header mismatch. Expected {EXPECTED_ROWS[0]}, got {actual_rows[0]}"

    # Check row count
    assert len(actual_rows) == len(EXPECTED_ROWS), f"CSV row count mismatch. Expected {len(EXPECTED_ROWS)} rows (including header), got {len(actual_rows)}"

    # Check content
    for i, (actual, expected) in enumerate(zip(actual_rows[1:], EXPECTED_ROWS[1:]), start=1):
        assert actual[0] == expected[0], f"Row {i}: device_name mismatch. Expected {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i}: timestamp mismatch. Expected {expected[1]}, got {actual[1]}"

        # Parse floats to handle minor formatting differences (e.g., 20.0 vs 20)
        try:
            actual_temp = float(actual[2])
            expected_temp = float(expected[2])
            assert abs(actual_temp - expected_temp) < 0.001, f"Row {i}: temperature mismatch. Expected {expected[2]}, got {actual[2]}"
        except ValueError:
            pytest.fail(f"Row {i}: temperature could not be parsed as float: {actual[2]}")

        try:
            actual_avg = float(actual[3])
            expected_avg = float(expected[3])
            assert abs(actual_avg - expected_avg) < 0.005, f"Row {i}: moving_avg mismatch. Expected {expected[3]}, got {actual[3]}"

            # Also check formatting if possible (must have 2 decimal places)
            parts = actual[3].split('.')
            if len(parts) == 2:
                assert len(parts[1]) == 2, f"Row {i}: moving_avg should be rounded to 2 decimal places, got {actual[3]}"
        except ValueError:
            pytest.fail(f"Row {i}: moving_avg could not be parsed as float: {actual[3]}")