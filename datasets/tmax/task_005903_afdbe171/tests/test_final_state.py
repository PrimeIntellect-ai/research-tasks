# test_final_state.py

import os
import json
import math
import pytest

def test_debug_report_exists_and_valid_json():
    path = "/home/user/debug_report.json"
    assert os.path.isfile(path), f"File missing: {path}"

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(data, dict), "JSON root must be an object (dictionary)."

def test_debug_report_contents():
    path = "/home/user/debug_report.json"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        data = json.load(f)

    assert "failing_function" in data, "Missing key: 'failing_function'"
    assert data["failing_function"] == "optimize_weights", f"Incorrect failing_function: {data['failing_function']}"

    assert "target_threshold" in data, "Missing key: 'target_threshold'"
    assert isinstance(data["target_threshold"], (int, float)), "target_threshold must be a number"
    assert math.isclose(data["target_threshold"], 3.14, rel_tol=1e-2, abs_tol=1e-2), f"Incorrect target_threshold: {data['target_threshold']}"

    assert "recovered_job_name" in data, "Missing key: 'recovered_job_name'"
    assert data["recovered_job_name"] == "DataProc_Alpha", f"Incorrect recovered_job_name: {data['recovered_job_name']}"