# test_final_state.py

import os
import csv
import pytest

PROCESSED_CSV = "/home/user/processed_sensors.csv"
SCRIPT_PATH = "/home/user/process_data.sh"

EXPECTED_DATA = [
    ["1000", "Rack1", "Humidity", "45.0", "45.00", "0.00"],
    ["1060", "Rack1", "Humidity", "45.2", "45.10", "0.10"],
    ["1120", "Rack1", "Humidity", "45.1", "45.10", "0.00"],
    ["1180", "Rack1", "Humidity", "46.0", "45.43", "0.57"],
    ["1240", "Rack1", "Humidity", "45.5", "45.53", "0.03"],
    ["1000", "Rack1", "Temperature", "22.0", "22.00", "0.00"],
    ["1060", "Rack1", "Temperature", "22.1", "22.05", "0.05"],
    ["1120", "Rack1", "Temperature", "22.5", "22.20", "0.30"],
    ["1180", "Rack1", "Temperature", "28.0", "24.20", "3.80"],
    ["1240", "Rack1", "Temperature", "22.2", "24.23", "2.03"],
    ["1000", "Rack2", "Humidity", "42.0", "42.00", "0.00"],
    ["1060", "Rack2", "Humidity", "42.1", "42.05", "0.05"],
    ["1120", "Rack2", "Humidity", "42.0", "42.03", "0.03"],
    ["1180", "Rack2", "Humidity", "42.2", "42.10", "0.10"],
    ["1240", "Rack2", "Humidity", "42.1", "42.10", "0.00"],
    ["1000", "Rack2", "Temperature", "23.5", "23.50", "0.00"],
    ["1060", "Rack2", "Temperature", "23.6", "23.55", "0.05"],
    ["1120", "Rack2", "Temperature", "23.7", "23.60", "0.10"],
    ["1180", "Rack2", "Temperature", "23.6", "23.63", "0.03"],
    ["1240", "Rack2", "Temperature", "23.8", "23.70", "0.10"]
]

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_processed_csv_exists():
    assert os.path.exists(PROCESSED_CSV), f"Output file {PROCESSED_CSV} does not exist."
    assert os.path.isfile(PROCESSED_CSV), f"Output path {PROCESSED_CSV} is not a file."

def test_processed_csv_format_and_content():
    with open(PROCESSED_CSV, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"File {PROCESSED_CSV} is empty.")

        expected_header = ["Timestamp", "RackID", "Metric", "Value", "MovingAvg", "Distance"]
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        rows = list(reader)

    assert len(rows) == len(EXPECTED_DATA), f"Expected {len(EXPECTED_DATA)} rows, but got {len(rows)}."

    for i, (actual_row, expected_row) in enumerate(zip(rows, EXPECTED_DATA)):
        assert len(actual_row) == 6, f"Row {i+1} does not have exactly 6 columns: {actual_row}"

        # Check string exact matches for string columns
        assert actual_row[0] == expected_row[0], f"Row {i+1} Timestamp mismatch: expected {expected_row[0]}, got {actual_row[0]}"
        assert actual_row[1] == expected_row[1], f"Row {i+1} RackID mismatch: expected {expected_row[1]}, got {actual_row[1]}"
        assert actual_row[2] == expected_row[2], f"Row {i+1} Metric mismatch: expected {expected_row[2]}, got {actual_row[2]}"

        # Check numeric values with float conversion to allow for minor format differences in Value (e.g. 45 vs 45.0)
        try:
            actual_val = float(actual_row[3])
            expected_val = float(expected_row[3])
            assert abs(actual_val - expected_val) < 1e-5, f"Row {i+1} Value mismatch: expected {expected_val}, got {actual_val}"
        except ValueError:
            pytest.fail(f"Row {i+1} Value '{actual_row[3]}' is not a valid float.")

        # MovingAvg and Distance must be formatted to exactly 2 decimal places
        assert "." in actual_row[4] and len(actual_row[4].split(".")[1]) == 2, f"Row {i+1} MovingAvg '{actual_row[4]}' not formatted to 2 decimal places."
        assert "." in actual_row[5] and len(actual_row[5].split(".")[1]) == 2, f"Row {i+1} Distance '{actual_row[5]}' not formatted to 2 decimal places."

        try:
            actual_ma = float(actual_row[4])
            expected_ma = float(expected_row[4])
            assert abs(actual_ma - expected_ma) < 1e-2, f"Row {i+1} MovingAvg mismatch: expected {expected_ma}, got {actual_ma}"

            actual_dist = float(actual_row[5])
            expected_dist = float(expected_row[5])
            assert abs(actual_dist - expected_dist) < 1e-2, f"Row {i+1} Distance mismatch: expected {expected_dist}, got {actual_dist}"
        except ValueError:
            pytest.fail(f"Row {i+1} MovingAvg/Distance contains invalid floats.")