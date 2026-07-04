# test_final_state.py

import os
import stat
import json
import math
import pytest

def test_executable_exists_and_compiled():
    exe_path = "/home/user/bin/score_calc"
    assert os.path.exists(exe_path), f"Executable not found at {exe_path}"
    assert os.path.isfile(exe_path), f"{exe_path} is not a file"

    # Check if it's executable
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_path} is not executable"

def test_result_json_exists():
    json_path = "/home/user/result.json"
    assert os.path.exists(json_path), f"Result file not found at {json_path}"
    assert os.path.isfile(json_path), f"{json_path} is not a file"

def test_result_json_content():
    json_path = "/home/user/result.json"
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{json_path} does not contain valid JSON")

    expected_keys = {"optimal_x", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, found {set(data.keys())}"

    # The expected values are derived from the analytical solution and numpy's random seed 42
    # optimal_x = 4.0000
    # ci_lower = 3.9161
    # ci_upper = 4.0931

    # Check optimal_x
    assert isinstance(data["optimal_x"], (int, float)), "optimal_x must be a number"
    assert math.isclose(data["optimal_x"], 4.0000, abs_tol=1e-4), f"Expected optimal_x to be 4.0000, got {data['optimal_x']}"

    # Check ci_lower
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a number"
    assert math.isclose(data["ci_lower"], 3.9161, abs_tol=1e-4), f"Expected ci_lower to be 3.9161, got {data['ci_lower']}"

    # Check ci_upper
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a number"
    assert math.isclose(data["ci_upper"], 4.0931, abs_tol=1e-4), f"Expected ci_upper to be 4.0931, got {data['ci_upper']}"