# test_final_state.py

import os
import math
import sys
import importlib.util

def test_test_optimize_file_exists_and_contains_test():
    test_file = "/home/user/project/test_optimize.py"
    assert os.path.exists(test_file), f"Test file not found: {test_file}"

    with open(test_file, "r") as f:
        content = f.read()
        assert "test_convergence" in content, "Test function 'test_convergence' is missing in test_optimize.py"
        assert "pytest" in content or "import pytest" in content or "optimize_function" in content, "test_optimize.py does not look like a proper test file"

def test_root_txt_contains_correct_value():
    root_file = "/home/user/root.txt"
    assert os.path.exists(root_file), f"Root output file not found: {root_file}"

    with open(root_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {root_file} is not a valid float string: '{content}'")

    expected_root = -1.7692923542386314
    assert math.isclose(val, expected_root, rel_tol=1e-3, abs_tol=1e-3), f"Incorrect root value in {root_file}: {val}. Expected approximately {expected_root}"

def test_optimize_script_is_fixed():
    opt_file = "/home/user/project/optimize.py"
    assert os.path.exists(opt_file), f"Script not found: {opt_file}"

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location("optimize", opt_file)
    optimize_module = importlib.util.module_from_spec(spec)
    sys.modules["optimize"] = optimize_module
    try:
        spec.loader.exec_module(optimize_module)
    except Exception as e:
        pytest.fail(f"Failed to import {opt_file}: {e}")

    assert hasattr(optimize_module, "optimize_function"), "optimize_function is missing in optimize.py"

    try:
        # Check if it converges without arguments
        result = optimize_module.optimize_function()
    except Exception as e:
        pytest.fail(f"optimize_function() raised an exception: {e}. The convergence issue might not be fixed.")

    expected_root = -1.7692923542386314
    assert math.isclose(result, expected_root, rel_tol=1e-3, abs_tol=1e-3), f"optimize_function() returned {result}, expected approximately {expected_root}"