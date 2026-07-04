# test_final_state.py

import os
import subprocess
import pytest

def test_test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Log file missing at {log_path}. Did you redirect the test output?"

def test_test_results_log_content():
    log_path = "/home/user/test_results.log"
    if not os.path.isfile(log_path):
        pytest.fail(f"Log file missing at {log_path}")

    with open(log_path, "r") as f:
        content = f.read()

    assert "OK" in content, "Log file does not show passing tests (missing 'OK')."

def test_python_script_execution():
    script_path = "/home/user/test_processor.py"
    assert os.path.isfile(script_path), f"Python test script missing at {script_path}"

    # Run the script to verify it actually passes now
    result = subprocess.run(
        ["python3", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Python tests failed to execute successfully. Exit code: {result.returncode}\nStderr: {result.stderr}"
    assert "OK" in result.stderr, "Output of python script does not indicate passing tests."

def test_python_script_fixed():
    script_path = "/home/user/test_processor.py"
    if not os.path.isfile(script_path):
        pytest.fail(f"Python test script missing at {script_path}")

    with open(script_path, "r") as f:
        content = f.read()

    assert "_pack_" in content, "The Record class in the Python script does not seem to have been packed (_pack_ missing)."