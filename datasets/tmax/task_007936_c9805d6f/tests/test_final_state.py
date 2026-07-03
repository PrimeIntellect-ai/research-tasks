# test_final_state.py

import os
import json
import math

def test_dataset_csv_exists():
    """Test that dataset.csv was generated."""
    file_path = "/home/user/dataset.csv"
    assert os.path.isfile(file_path), f"Missing file: {file_path}. Did you run datagen?"

def test_solver_go_exists_and_uses_cholesky():
    """Test that solver.go exists and uses Cholesky decomposition from gonum."""
    file_path = "/home/user/solver.go"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read()

    assert "Cholesky" in content, "solver.go does not seem to use Cholesky decomposition as required."
    assert "gonum.org/v1/gonum/mat" in content, "solver.go does not import gonum.org/v1/gonum/mat."

def test_results_json_values():
    """Test that results.json contains the correct statistical estimates."""
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} is not valid JSON."

    expected_values = {
        "beta0": 2.4667,
        "beta1": -1.5000,
        "beta2": 3.0000,
        "f_stat": 166724.8148
    }

    for key, expected_val in expected_values.items():
        assert key in results, f"Key '{key}' missing in {file_path}"
        actual_val = results[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."
        assert math.isclose(actual_val, expected_val, abs_tol=0.001), \
            f"Value for '{key}' is {actual_val}, expected approximately {expected_val}"