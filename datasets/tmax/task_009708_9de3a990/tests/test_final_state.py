# test_final_state.py

import os
import json
import pytest

RESULTS_FILE = "/home/user/project/results.jsonl"

def test_results_file_exists():
    """Check if the results file was generated."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist. Did you run the script?"

def test_results_content():
    """Check if the results file contains the correct calculated cube roots."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist."

    expected_results = {
        "A1": 2.0,
        "B2": 3.0,
        "C3": 5.0,
        "D4": 4.0
    }

    actual_results = {}
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {RESULTS_FILE} is not valid JSON: {line}")

            assert "id" in data, f"Missing 'id' key in line {line_num}: {line}"
            assert "cube_root" in data, f"Missing 'cube_root' key in line {line_num}: {line}"

            actual_results[data["id"]] = data["cube_root"]

    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} records, but found {len(actual_results)}."

    for req_id, expected_val in expected_results.items():
        assert req_id in actual_results, f"Missing result for id '{req_id}'"
        actual_val = actual_results[req_id]
        assert isinstance(actual_val, (int, float)), f"Value for '{req_id}' is not a number: {actual_val}"
        assert abs(actual_val - expected_val) < 1e-4, f"Incorrect cube root for '{req_id}'. Expected {expected_val}, got {actual_val}"