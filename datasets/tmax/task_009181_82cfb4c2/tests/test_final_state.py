# test_final_state.py

import os
import csv
import json
import pytest

def test_clean_data_csv():
    csv_path = '/home/user/clean_data.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    expected_rows = [
        ['date', 'unit', 'temperature_c', 'pressure_kpa'],
        ['2023-10-01', 'Unit-Alpha', '40.0', '100.0'],
        ['2023-10-02', 'Unit-Beta', '40.0', '100.0'],
        ['2023-10-03', 'Unit-Gamma', '35.3', '104.8'],
        ['2023-10-04', 'Unit-Delta', '22.0', '101.3'],
        ['2022-12-31', 'Unit-Epsilon', '0.0', '101.4'],
        ['2023-01-01', 'Unit-Zeta', '0.0', '0.0']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, f"{csv_path} is empty."
    assert actual_rows[0] == expected_rows[0], f"CSV header is incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}"

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows (including header), got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, got {actual}"


def test_pipeline_json():
    json_path = '/home/user/pipeline.json'
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    expected_data = {
        "total_lines_processed": 8,
        "successful_parses": 6,
        "failed_parses": 2
    }

    assert isinstance(data, dict), f"JSON root must be an object/dict."

    for key, expected_value in expected_data.items():
        assert key in data, f"Key '{key}' missing from {json_path}."
        assert data[key] == expected_value, f"Value for '{key}' is incorrect. Expected {expected_value}, got {data[key]}."