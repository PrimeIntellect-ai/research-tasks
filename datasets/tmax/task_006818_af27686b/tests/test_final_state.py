# test_final_state.py
import os
import json
import math
import pytest

def test_cpp_source_exists():
    path = "/home/user/analyze_energies.cpp"
    assert os.path.isfile(path), f"C++ source file {path} is missing."

def test_executable_exists():
    path = "/home/user/analyze_energies"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_json_results_exist_and_valid():
    path = "/home/user/analysis_results.json"
    assert os.path.isfile(path), f"Results file {path} is missing."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_keys = {
        "mean", "variance", "log_likelihood_gaussian",
        "log_likelihood_exponential", "aic_gaussian",
        "aic_exponential", "best_fit"
    }

    missing_keys = expected_keys - results.keys()
    assert not missing_keys, f"JSON results are missing keys: {missing_keys}"

def test_json_results_values():
    path = "/home/user/analysis_results.json"
    if not os.path.isfile(path):
        pytest.skip("JSON file missing")

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Invalid JSON")

    # Due to stdlib-only constraints, we verify against the known generated values
    # from the fixed random seed in the setup script.

    assert math.isclose(results.get("mean", 0), 4.99757, rel_tol=1e-3, abs_tol=1e-2), \
        f"Mean value {results.get('mean')} is incorrect."

    assert math.isclose(results.get("variance", 0), 1.44229, rel_tol=1e-3, abs_tol=1e-2), \
        f"Variance value {results.get('variance')} is incorrect."

    assert math.isclose(results.get("log_likelihood_gaussian", 0), -15949.72, rel_tol=1e-3, abs_tol=1.0), \
        f"Gaussian Log-Likelihood {results.get('log_likelihood_gaussian')} is incorrect."

    assert math.isclose(results.get("log_likelihood_exponential", 0), -26090.73, rel_tol=1e-3, abs_tol=1.0), \
        f"Exponential Log-Likelihood {results.get('log_likelihood_exponential')} is incorrect."

    assert math.isclose(results.get("aic_gaussian", 0), 31903.44, rel_tol=1e-3, abs_tol=1.0), \
        f"Gaussian AIC {results.get('aic_gaussian')} is incorrect."

    assert math.isclose(results.get("aic_exponential", 0), 52183.46, rel_tol=1e-3, abs_tol=1.0), \
        f"Exponential AIC {results.get('aic_exponential')} is incorrect."

    best_fit = results.get("best_fit", "")
    assert isinstance(best_fit, str) and best_fit.lower() == "gaussian", \
        f"Best fit should be 'gaussian', got '{best_fit}'."