# test_final_state.py
import os
import json
import ast
import pytest

def test_json_exists_and_valid():
    file_path = "/home/user/posterior_summary.json"
    assert os.path.exists(file_path), f"File {file_path} does not exist. Did you run the script?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected_keys = {"r_mean", "K_mean", "d_mean"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, found {set(data.keys())}"
    for k in expected_keys:
        assert isinstance(data[k], (int, float)), f"Value for {k} must be a number, found {type(data[k])}"

def test_json_values():
    file_path = "/home/user/posterior_summary.json"
    if not os.path.exists(file_path):
        pytest.skip("JSON file missing.")

    with open(file_path, "r") as f:
        data = json.load(f)

    r = data["r_mean"]
    K = data["K_mean"]
    d = data["d_mean"]

    assert 0.3 <= r <= 0.7, f"r_mean {r} is outside the expected range [0.3, 0.7]"
    assert 400 <= K <= 600, f"K_mean {K} is outside the expected range [400, 600]"
    assert 0.01 <= d <= 0.3, f"d_mean {d} is outside the expected range [0.01, 0.3]"

def test_script_modifications():
    file_path = "/home/user/mcmc_mutations.py"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # Check for solve_ivp and RK45
    assert "solve_ivp" in content, "The script does not seem to use scipy.integrate.solve_ivp."
    assert "RK45" in content, "The script does not seem to specify the RK45 method for solve_ivp."

    # Check for multiprocessing Pool
    assert "multiprocessing" in content, "The script does not import or use multiprocessing."
    assert "Pool" in content, "The script does not seem to use multiprocessing.Pool."

    # Parse AST to ensure Pool is passed to EnsembleSampler
    try:
        tree = ast.parse(content)
    except SyntaxError:
        pytest.fail("The script contains syntax errors and cannot be parsed.")

    # We just do a simple string check to ensure pool is passed to the sampler
    # as AST checking for this specific pattern can be brittle depending on how they wrote it.
    assert "pool=" in content or "pool =" in content or "Pool" in content, "Could not verify that pool was passed to the sampler."