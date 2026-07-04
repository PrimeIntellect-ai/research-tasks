# test_final_state.py

import os
import json
import pytest

def test_analyze_go_exists():
    file_path = "/home/user/analyze.go"
    assert os.path.isfile(file_path), f"Expected Go program {file_path} does not exist."

def test_validation_errors_log():
    file_path = "/home/user/validation_errors.log"
    assert os.path.isfile(file_path), f"Expected file {file_path} was not generated."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_errors = ["W", "X", "Y", "Z"]
    assert lines == expected_errors, f"Content of {file_path} does not match the expected missing nodes. Got: {lines}"

def test_summary_json():
    file_path = "/home/user/summary.json"
    assert os.path.isfile(file_path), f"Expected file {file_path} was not generated."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    expected_data = {
        "total_queries": 5,
        "successful_paths": 4,
        "total_cost": 110,
        "average_cost": 27.5
    }

    assert "total_queries" in data, "Missing 'total_queries' in summary.json"
    assert data["total_queries"] == expected_data["total_queries"], f"Expected total_queries to be {expected_data['total_queries']}, got {data['total_queries']}"

    assert "successful_paths" in data, "Missing 'successful_paths' in summary.json"
    assert data["successful_paths"] == expected_data["successful_paths"], f"Expected successful_paths to be {expected_data['successful_paths']}, got {data['successful_paths']}"

    assert "total_cost" in data, "Missing 'total_cost' in summary.json"
    assert data["total_cost"] == expected_data["total_cost"], f"Expected total_cost to be {expected_data['total_cost']}, got {data['total_cost']}"

    assert "average_cost" in data, "Missing 'average_cost' in summary.json"
    assert data["average_cost"] == expected_data["average_cost"], f"Expected average_cost to be {expected_data['average_cost']}, got {data['average_cost']}"