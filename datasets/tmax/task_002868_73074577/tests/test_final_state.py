# test_final_state.py

import os
import json
import pytest

def test_submission_result_exists():
    result_path = "/home/user/submission_result.json"
    assert os.path.isfile(result_path), f"Expected submission result file at {result_path} is missing."

def test_submission_result_mse():
    result_path = "/home/user/submission_result.json"
    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert "mse" in data, f"Key 'mse' not found in {result_path}. Found keys: {list(data.keys())}"

    mse_value = data["mse"]
    assert isinstance(mse_value, (int, float)), f"MSE value must be a number, got {type(mse_value)}"

    threshold = 0.05
    assert mse_value <= threshold, f"MSE {mse_value} is greater than the required threshold {threshold}."

def test_start_services_fixed():
    script_path = "/app/start_services.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "REDIS_HOST" in content, "REDIS_HOST is still missing from start_services.sh"