# test_final_state.py

import os
import json
import pytest

def test_result_json_exists_and_valid():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing result file: {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON")

    assert "changepoint_index" in data, "Key 'changepoint_index' not found in result.json"

    try:
        predicted = int(data["changepoint_index"])
    except (ValueError, TypeError):
        pytest.fail("Value for 'changepoint_index' must be an integer")

    expected = 3450
    error = abs(predicted - expected)

    assert error <= 5, f"Changepoint index error is {error} (predicted: {predicted}, expected: {expected}). Must be <= 5."