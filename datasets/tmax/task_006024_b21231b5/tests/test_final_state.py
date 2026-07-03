# test_final_state.py

import os
import json
import stat
import pytest

def test_files_exist_and_permissions():
    """Check that required files exist and run_pipeline.sh is executable."""
    analyze_path = "/home/user/analyze.py"
    test_analyze_path = "/home/user/test_analyze.py"
    run_pipeline_path = "/home/user/run_pipeline.sh"

    assert os.path.isfile(analyze_path), f"Missing {analyze_path}"
    assert os.path.isfile(test_analyze_path), f"Missing {test_analyze_path}"
    assert os.path.isfile(run_pipeline_path), f"Missing {run_pipeline_path}"

    # Check if run_pipeline.sh is executable
    st = os.stat(run_pipeline_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{run_pipeline_path} is not executable"

def test_results_json_keys_and_values():
    """Check results.json exists, has exact keys, and values are within expected ranges."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Missing {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file.")

    expected_keys = {"opt_C", "opt_k", "factor_x", "mcmc_C", "mcmc_k"}
    assert set(results.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(results.keys())}"

    # Based on the ground truth generation:
    # true_C = 0.55, true_k = 0.3
    # factor_x for C=0.55 is approx 0.264

    opt_C = results["opt_C"]
    opt_k = results["opt_k"]
    factor_x = results["factor_x"]
    mcmc_C = results["mcmc_C"]
    mcmc_k = results["mcmc_k"]

    # Check types
    assert isinstance(opt_C, (int, float)), "opt_C must be a number"
    assert isinstance(opt_k, (int, float)), "opt_k must be a number"
    assert isinstance(factor_x, (int, float)), "factor_x must be a number"
    assert isinstance(mcmc_C, (int, float)), "mcmc_C must be a number"
    assert isinstance(mcmc_k, (int, float)), "mcmc_k must be a number"

    # Check bounds (allowing some tolerance for noise and MCMC variance)
    assert 0.45 < opt_C < 0.65, f"opt_C {opt_C} is out of expected range (0.45, 0.65)"
    assert 0.2 < opt_k < 0.4, f"opt_k {opt_k} is out of expected range (0.2, 0.4)"

    # factor_x should satisfy x^3 + 2x - opt_C = 0
    # We can check the equation directly instead of hardcoding the expected root
    equation_val = factor_x**3 + 2*factor_x - opt_C
    assert abs(equation_val) < 1e-3, f"factor_x {factor_x} does not satisfy x^3 + 2x - C = 0 for C={opt_C}"

    assert 0.45 < mcmc_C < 0.65, f"mcmc_C {mcmc_C} is out of expected range (0.45, 0.65)"
    assert 0.2 < mcmc_k < 0.4, f"mcmc_k {mcmc_k} is out of expected range (0.2, 0.4)"

def test_test_analyze_py_contents():
    """Verify that test_analyze.py contains the required test functions."""
    test_analyze_path = "/home/user/test_analyze.py"
    with open(test_analyze_path, "r") as f:
        content = f.read()

    assert "def test_solve_structural" in content, "Missing test_solve_structural() in test_analyze.py"
    assert "def test_optimize_params" in content, "Missing test_optimize_params() in test_analyze.py"
    assert "pytest" in content, "pytest is not imported or used in test_analyze.py"

def test_run_pipeline_contents():
    """Verify that run_pipeline.sh contains required commands."""
    run_pipeline_path = "/home/user/run_pipeline.sh"
    with open(run_pipeline_path, "r") as f:
        content = f.read()

    assert "pip" in content and "install" in content, "run_pipeline.sh does not install dependencies"
    assert "pytest" in content, "run_pipeline.sh does not run pytest"
    assert "python" in content and "analyze.py" in content, "run_pipeline.sh does not execute analyze.py"