# test_final_state.py

import os
import sys
import importlib.util
import pytest

APP_DIR = "/home/user/app"
COMPUTATION_PY = os.path.join(APP_DIR, "computation.py")
ENV_SH = os.path.join(APP_DIR, "env.sh")
TEST_COMPUTATION_PY = os.path.join(APP_DIR, "test_computation.py")
TEST_RESULTS_LOG = os.path.join(APP_DIR, "test_results.log")

def test_computation_py_fixed():
    assert os.path.isfile(COMPUTATION_PY), f"File missing: {COMPUTATION_PY}"
    with open(COMPUTATION_PY, "r") as f:
        content = f.read()

    # Check if a max shift is implemented
    assert "max" in content, "The log-sum-exp trick requires finding the maximum value (e.g., using np.max or max)."

    # Dynamically load and test the function
    spec = importlib.util.spec_from_file_location("computation", COMPUTATION_PY)
    computation = importlib.util.module_from_spec(spec)
    sys.modules["computation"] = computation
    spec.loader.exec_module(computation)

    import numpy as np
    x = np.array([1000.0, 1000.0])
    result = computation.compute_log_sum_exp(x)
    assert not np.isinf(result), "compute_log_sum_exp still returns inf for large inputs."
    assert np.isclose(result, 1000.6931471805599), f"compute_log_sum_exp returned incorrect value: {result}"

    x_large = np.array([5000.0, 5001.0])
    result_large = computation.compute_log_sum_exp(x_large)
    assert not np.isinf(result_large), "compute_log_sum_exp overflows for very large inputs."
    assert np.isclose(result_large, 5001.313261687518), f"compute_log_sum_exp returned incorrect value for large input: {result_large}"

def test_env_sh_fixed():
    assert os.path.isfile(ENV_SH), f"File missing: {ENV_SH}"
    with open(ENV_SH, "r") as f:
        content = f.read()

    expected_vars = [
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS"
    ]
    for var in expected_vars:
        assert f"{var}=4" in content, f"Expected {var}=4 in {ENV_SH}"

def test_test_computation_py_exists_and_valid():
    assert os.path.isfile(TEST_COMPUTATION_PY), f"File missing: {TEST_COMPUTATION_PY}"
    with open(TEST_COMPUTATION_PY, "r") as f:
        content = f.read()

    assert "test_log_sum_exp" in content, "test_log_sum_exp missing in test_computation.py"
    assert "test_log_sum_exp_large" in content, "test_log_sum_exp_large missing in test_computation.py"
    assert "computation" in content, "computation module not imported in test_computation.py"

def test_test_results_log_exists():
    assert os.path.isfile(TEST_RESULTS_LOG), f"File missing: {TEST_RESULTS_LOG}. Did you run pytest and redirect the output?"
    with open(TEST_RESULTS_LOG, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"{TEST_RESULTS_LOG} is empty."