# test_final_state.py
import os
import sys
import subprocess
import importlib.util

TICKET_DIR = "/home/user/ticket_4489"

def test_resolution_file():
    """Check that resolution.txt exists and contains 'RESOLVED'."""
    res_path = os.path.join(TICKET_DIR, "resolution.txt")
    assert os.path.isfile(res_path), f"{res_path} is missing."
    with open(res_path, "r") as f:
        content = f.read().strip()
    assert content == "RESOLVED", f"Expected 'RESOLVED' in resolution.txt, got '{content}'."

def test_summarize_py_fixes():
    """Check that summarize.py has been modified to fix the bugs."""
    summarize_path = os.path.join(TICKET_DIR, "summarize.py")
    assert os.path.isfile(summarize_path), f"{summarize_path} is missing."

    # Load summarize.py dynamically
    spec = importlib.util.spec_from_file_location("summarize", summarize_path)
    summarize = importlib.util.module_from_spec(spec)
    sys.modules["summarize"] = summarize
    try:
        spec.loader.exec_module(summarize)
    except Exception as e:
        assert False, f"Failed to load summarize.py: {e}"

    # 1. Precision Error Fix
    try:
        result_sum = summarize.sum_values([0.1] * 10)
    except Exception as e:
        assert False, f"sum_values raised an exception: {e}"

    assert result_sum == 1.0, f"Precision error not fixed. sum_values([0.1]*10) returned {result_sum} instead of 1.0."

    # 2. Intermittent Crashes Fix (Boundary condition)
    try:
        # If the off-by-one is not fixed, this may segfault or return garbage
        # We test it with a specific length to see if it survives
        result_fast = summarize.fast_process([1.0] * 10)
        assert isinstance(result_fast, float), "fast_process should return a float."
    except Exception as e:
        assert False, f"fast_process raised an exception: {e}"


def test_regression_script():
    """Check that test_regression.py exists and runs successfully."""
    script_path = os.path.join(TICKET_DIR, "test_regression.py")
    assert os.path.isfile(script_path), f"{script_path} is missing."

    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_regression.py failed to run. Stderr: {result.stderr}"


def test_fuzzer_script():
    """Check that fuzzer.py exists and runs successfully."""
    script_path = os.path.join(TICKET_DIR, "fuzzer.py")
    assert os.path.isfile(script_path), f"{script_path} is missing."

    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"fuzzer.py failed to run. Stderr: {result.stderr}"