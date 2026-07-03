# test_final_state.py

import os
import csv
import json
import pytest
import math

def test_processed_features_csv_exists():
    """Test that the processed_features.csv file exists."""
    file_path = '/home/user/processed_features.csv'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_pipeline_log_json_exists():
    """Test that the pipeline_log.json file exists."""
    file_path = '/home/user/pipeline_log.json'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_processed_features_csv_content():
    """Test the contents of the processed_features.csv file."""
    file_path = '/home/user/processed_features.csv'

    expected_rows = [
        [0, -1.4639, -1.4639, -1.4639, -1.4639],
        [1, -0.8783, -0.8783, -1.1711, -1.1711],
        [2, -0.2928, -0.2928, -0.8783, -0.8783],
        [3, 0.2928, 0.2928, -0.5855, -0.5855],
        [4, 0.8783, 0.8783, -0.2928, -0.2928],
        [5, 1.4639, 1.4639, 0.2928, 0.2928]
    ]

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_header = ["time_min", "norm_temp", "norm_hum", "roll_mean_temp", "roll_mean_hum"]
        assert header == expected_header, f"CSV header {header} does not match expected {expected_header}"

        rows = list(reader)
        assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(rows)}"

        for i, row in enumerate(rows):
            assert int(row[0]) == expected_rows[i][0], f"Row {i} time_min mismatch: {row[0]} != {expected_rows[i][0]}"
            for j in range(1, 5):
                val = float(row[j])
                expected_val = expected_rows[i][j]
                assert math.isclose(val, expected_val, abs_tol=0.0002), f"Row {i} column {header[j]} mismatch: {val} != {expected_val}"

def test_pipeline_log_json_content():
    """Test the contents of the pipeline_log.json file."""
    file_path = '/home/user/pipeline_log.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert data.get("total_rows_input") == 3, f"Expected total_rows_input to be 3, got {data.get('total_rows_input')}"
    assert data.get("total_rows_output") == 6, f"Expected total_rows_output to be 6, got {data.get('total_rows_output')}"

    assert math.isclose(data.get("temperature_mean", 0), 22.5000, abs_tol=0.0002), "temperature_mean mismatch"
    assert math.isclose(data.get("temperature_stddev", 0), 1.7078, abs_tol=0.0002), "temperature_stddev mismatch"
    assert math.isclose(data.get("humidity_mean", 0), 52.5000, abs_tol=0.0002), "humidity_mean mismatch"
    assert math.isclose(data.get("humidity_stddev", 0), 1.7078, abs_tol=0.0002), "humidity_stddev mismatch"