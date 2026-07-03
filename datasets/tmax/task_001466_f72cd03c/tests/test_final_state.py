# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/validate_plugins.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

def test_load_plan_exists():
    plan_path = "/home/user/load_plan.json"
    assert os.path.isfile(plan_path), f"Load plan JSON file {plan_path} is missing."

def test_load_plan_content():
    plan_path = "/home/user/load_plan.json"
    try:
        with open(plan_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {plan_path} does not contain valid JSON.")

    expected_data = {
        "libalpha.so": True,
        "libbeta.so": False,
        "libgamma.so": True
    }

    assert isinstance(data, dict), "Load plan JSON should be a dictionary."
    assert data == expected_data, f"Load plan content is incorrect. Expected {expected_data}, but got {data}."