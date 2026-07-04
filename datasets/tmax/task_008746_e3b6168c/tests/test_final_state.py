# test_final_state.py
import os
import json
import math

def test_virtual_environment_exists():
    """Check if the Python virtual environment was created at the specified path."""
    venv_dir = "/home/user/analysis_env"
    assert os.path.isdir(venv_dir), f"Virtual environment directory not found at {venv_dir}"

    # Check for the python executable in the bin directory (standard for venv on Linux)
    python_bin = os.path.join(venv_dir, "bin", "python")
    python3_bin = os.path.join(venv_dir, "bin", "python3")

    assert os.path.isfile(python_bin) or os.path.isfile(python3_bin), \
        f"Python executable not found in {os.path.join(venv_dir, 'bin')}. Ensure the virtual environment is correctly created."

def test_results_json_exists_and_correct():
    """Check if results.json exists, is valid JSON, and contains the correct computed values."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file missing at {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {results_path} does not contain valid JSON."

    # Check keys
    assert "wasserstein_distance" in data, "Key 'wasserstein_distance' is missing in results.json"
    assert "regression_slope" in data, "Key 'regression_slope' is missing in results.json"

    w_dist = data["wasserstein_distance"]
    r_slope = data["regression_slope"]

    # Check types
    assert isinstance(w_dist, (int, float)), f"'wasserstein_distance' must be a number, got {type(w_dist).__name__}"
    assert isinstance(r_slope, (int, float)), f"'regression_slope' must be a number, got {type(r_slope).__name__}"

    # Check values based on ground truth
    expected_w_dist = 20.0
    expected_r_slope = 5.0

    assert math.isclose(w_dist, expected_w_dist, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected 'wasserstein_distance' to be approximately {expected_w_dist}, but got {w_dist}"

    assert math.isclose(r_slope, expected_r_slope, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected 'regression_slope' to be approximately {expected_r_slope}, but got {r_slope}"