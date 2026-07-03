# test_final_state.py

import os
import sys
import ast
import pytest

def test_bad_file():
    path = "/home/user/sim_project/bad_file.txt"
    assert os.path.exists(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert "input_037.txt" in content, "bad_file.txt does not contain the correct filename (input_037.txt)."

def test_utils_stability():
    sys.path.insert(0, "/home/user/sim_project")
    try:
        import utils
    except ImportError:
        pytest.fail("Could not import utils.py from /home/user/sim_project")

    try:
        # The max-shift trick should prevent OverflowError for large values
        res = utils.compute_weights([1000.0, 1000.0])
        assert len(res) == 2, "compute_weights should return a list of the same length as the input."
        assert abs(res[0] - 0.5) < 1e-6, "compute_weights returned incorrect probabilities."
        assert abs(res[1] - 0.5) < 1e-6, "compute_weights returned incorrect probabilities."
    except OverflowError:
        pytest.fail("compute_weights still raises OverflowError for large inputs. The numerical instability is not fixed.")
    finally:
        sys.path.pop(0)

def test_main_fd_leak_fixed():
    path = "/home/user/sim_project/main.py"
    assert os.path.exists(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read()

    # A robust check for the FD leak fix: we look for either a call to `.close()` or the use of `with open`
    # Since the original code had `f = open(...)` without `f.close()`, fixing it requires one of these.
    has_close = ".close(" in content
    has_with_open = "with open(" in content

    assert has_close or has_with_open, "main.py does not appear to fix the file descriptor leak. No .close() or 'with open' found."

def test_regression_test_exists():
    path = "/home/user/sim_project/test_regression.py"
    assert os.path.exists(path), f"Missing regression test file: {path}"
    with open(path, "r") as f:
        content = f.read()

    assert "test_stability" in content, "test_regression.py is missing the 'test_stability' function."
    assert "compute_weights" in content, "test_regression.py does not import or use 'compute_weights'."

def test_aggregate_result():
    path = "/home/user/sim_project/aggregate_result.txt"
    assert os.path.exists(path), f"Missing final output file: {path}. Did main.py run successfully to completion?"
    with open(path, "r") as f:
        content = f.read().strip()

    # 50 files, each returning a sum of probabilities (which is 1.0), so 50 * 1.0 = 50.0
    assert "Total: 50.00" in content, f"aggregate_result.txt has incorrect content. Expected 'Total: 50.00', got: '{content}'"