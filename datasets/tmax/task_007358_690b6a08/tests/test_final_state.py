# test_final_state.py

import os
import subprocess
import pytest

def test_fixed_blackbox_exists():
    """Check if the fixed Python script exists."""
    assert os.path.isfile("/home/user/fixed_blackbox.py"), "The file /home/user/fixed_blackbox.py is missing."

def test_test_sh_exists_and_executable():
    """Check if test.sh exists and is executable."""
    test_sh = "/home/user/test.sh"
    assert os.path.isfile(test_sh), f"The file {test_sh} is missing."
    assert os.access(test_sh, os.X_OK), f"The file {test_sh} is not executable."

def test_test_sh_execution_and_result():
    """Run test.sh and verify the output in result.log."""
    test_sh = "/home/user/test.sh"
    result_log = "/home/user/result.log"

    # Ensure result.log is removed before running to verify test.sh actually creates it
    if os.path.exists(result_log):
        os.remove(result_log)

    # Run the test script
    try:
        subprocess.run([test_sh], check=True, cwd="/home/user", capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {test_sh} failed with return code {e.returncode}.\nStderr: {e.stderr}")

    assert os.path.isfile(result_log), f"The file {result_log} was not created by {test_sh}."

    with open(result_log, "r") as f:
        content = f.read().strip()

    assert content == "1.0", f"Expected result.log to contain exactly '1.0', but found: {repr(content)}"