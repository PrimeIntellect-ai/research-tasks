# test_final_state.py
import os
import json
import math

def test_integrator_cpp_fixed():
    cpp_path = "/home/user/integrator.cpp"
    assert os.path.exists(cpp_path), f"{cpp_path} does not exist."
    with open(cpp_path, "r") as f:
        content = f.read()

    # Check that the bug is fixed
    assert "std::sqrt(tol / error)" in content, "The step-size adaptation bug in integrator.cpp was not fixed correctly. Expected 'std::sqrt(tol / error)'."
    assert "std::sqrt(error / tol)" not in content, "The buggy line 'std::sqrt(error / tol)' is still present in integrator.cpp."

def test_shared_library_exists():
    so_path = "/home/user/libintegrator.so"
    assert os.path.exists(so_path), f"Shared library {so_path} does not exist. Did you compile the C++ code?"

def test_python_script_exists():
    py_path = "/home/user/run_analysis.py"
    assert os.path.exists(py_path), f"Python script {py_path} does not exist."

def test_analysis_json():
    json_path = "/home/user/analysis.json"
    assert os.path.exists(json_path), f"Output file {json_path} does not exist."

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"{json_path} is not a valid JSON file."

    expected_keys = ["1e-2", "1e-3", "1e-4"]
    for key in expected_keys:
        assert key in data, f"Key '{key}' is missing from {json_path}."
        assert "steps" in data[key], f"'steps' missing for tolerance {key}."
        assert "error" in data[key], f"'error' missing for tolerance {key}."

        assert isinstance(data[key]["steps"], int), f"'steps' for {key} must be an integer."
        assert isinstance(data[key]["error"], (int, float)), f"'error' for {key} must be a number."

    # Validate the results based on expected behavior
    # Steps should be reasonably small (not hitting max_steps limit)
    assert data["1e-2"]["steps"] < 1000, "Number of steps for 1e-2 is too high, indicating the bug might not be fully resolved or the integrator diverged."
    assert data["1e-3"]["steps"] < 1000, "Number of steps for 1e-3 is too high."
    assert data["1e-4"]["steps"] < 2000, "Number of steps for 1e-4 is too high."

    # Errors should roughly decrease as tolerance decreases
    err_1 = data["1e-2"]["error"]
    err_2 = data["1e-3"]["error"]
    err_3 = data["1e-4"]["error"]

    assert err_1 > err_2, f"Error for 1e-2 ({err_1}) should be greater than error for 1e-3 ({err_2})."
    assert err_2 > err_3, f"Error for 1e-3 ({err_2}) should be greater than error for 1e-4 ({err_3})."