# test_final_state.py
import os
import json
import math

def test_cpp_file_exists():
    path = '/home/user/validate_etl.cpp'
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_executable_exists():
    path = '/home/user/validate_etl'
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_json_output():
    path = '/home/user/validation_result.json'
    assert os.path.exists(path), f"JSON output file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert "status" in res, "Missing 'status' key in JSON output."
    assert "r_point" in res, "Missing 'r_point' key in JSON output."
    assert "ci_lower" in res, "Missing 'ci_lower' key in JSON output."
    assert "ci_upper" in res, "Missing 'ci_upper' key in JSON output."

    assert res["status"] == "INVALID", f"Expected status 'INVALID', got '{res['status']}'"

    assert math.isclose(res["r_point"], 0.7844, abs_tol=0.001), f"Expected r_point ~0.7844, got {res['r_point']}"
    assert math.isclose(res["ci_lower"], 0.7513, abs_tol=0.005), f"Expected ci_lower ~0.7513, got {res['ci_lower']}"
    assert math.isclose(res["ci_upper"], 0.8146, abs_tol=0.005), f"Expected ci_upper ~0.8146, got {res['ci_upper']}"