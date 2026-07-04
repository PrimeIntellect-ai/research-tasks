# test_final_state.py

import os
import csv
import math
import pytest

def test_source_file_exists():
    path = "/home/user/validate_artifacts.cpp"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_executable_exists():
    path = "/home/user/validate_artifacts"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_validation_report_exists():
    path = "/home/user/experiments/validation_report.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_validation_report_content():
    path = "/home/user/experiments/validation_report.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Validation report is empty."

    header = rows[0]
    assert header == ["model_id", "is_valid", "distance"], f"Incorrect header: {header}"

    expected = {
        "model_A": (1, 0.0000),
        "model_B": (1, math.sqrt(5)),
        "model_C": (0, -1.0000),
        "model_D": (0, -1.0000),
        "model_E": (1, math.sqrt(5)),
    }

    data_rows = rows[1:]
    assert len(data_rows) == 5, f"Expected 5 data rows, got {len(data_rows)}"

    seen_models = set()
    for row in data_rows:
        assert len(row) == 3, f"Row does not have exactly 3 columns: {row}"
        model_id, is_valid_str, distance_str = row

        assert model_id in expected, f"Unexpected model_id: {model_id}"
        seen_models.add(model_id)

        expected_is_valid, expected_distance = expected[model_id]

        assert int(is_valid_str) == expected_is_valid, f"Incorrect is_valid for {model_id}: expected {expected_is_valid}, got {is_valid_str}"

        distance = float(distance_str)
        assert abs(distance - expected_distance) < 1e-3, f"Incorrect distance for {model_id}: expected ~{expected_distance:.4f}, got {distance}"

        # Check formatting: exactly 4 decimal places
        if "." in distance_str:
            decimals = len(distance_str.split(".")[1])
            assert decimals == 4, f"Distance for {model_id} not formatted to exactly 4 decimal places: {distance_str}"
        else:
            pytest.fail(f"Distance for {model_id} does not contain a decimal point: {distance_str}")

    assert seen_models == set(expected.keys()), "Not all expected models were found in the report."