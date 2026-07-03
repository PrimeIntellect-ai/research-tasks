# test_final_state.py

import os
import sys
import pytest
import importlib

def test_ceval_module_importable_and_functional():
    sys.path.insert(0, "/home/user/pricing_engine")
    try:
        import ceval
    except ImportError:
        pytest.fail("The 'ceval' module could not be imported. Did you fix setup.py and install the package?")

    try:
        result = ceval.eval_expr("MUL 3 4")
        assert result == 12, f"Expected ceval.eval_expr('MUL 3 4') to return 12, got {result}"
    except Exception as e:
        pytest.fail(f"Calling ceval.eval_expr failed: {e}")

def test_test_engine_py_exists_and_contains_tests():
    path = "/home/user/pricing_engine/test_engine.py"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "test_version_too_low" in content, "test_engine.py is missing 'test_version_too_low'"
    assert "test_evaluate_success" in content, "test_engine.py is missing 'test_evaluate_success'"
    assert "patch" in content, "test_engine.py does not seem to use 'patch' from unittest.mock"

def test_run_tests_sh_exists_and_executable():
    path = "/home/user/pricing_engine/run_tests.sh"
    assert os.path.isfile(path), f"Script {path} does not exist"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"

def test_test_results_log_contains_success():
    path = "/home/user/pricing_engine/test_results.log"
    assert os.path.isfile(path), f"Log file {path} does not exist. Did you run the tests and redirect output?"

    with open(path, "r") as f:
        content = f.read()

    assert "test_version_too_low" in content, "test_results.log does not mention 'test_version_too_low'"
    assert "test_evaluate_success" in content, "test_results.log does not mention 'test_evaluate_success'"
    assert "2 passed" in content or "2 successful" in content, "test_results.log does not indicate that 2 tests passed"