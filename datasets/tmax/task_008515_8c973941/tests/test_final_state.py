# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/rate_limit.sh"
TEST_SCRIPT_PATH = "/home/user/test_limiter.py"

def test_files_exist():
    """Verify that both required files exist."""
    assert os.path.isfile(SCRIPT_PATH), f"Missing script: {SCRIPT_PATH}"
    assert os.path.isfile(TEST_SCRIPT_PATH), f"Missing test script: {TEST_SCRIPT_PATH}"

def test_script_is_executable():
    """Verify that the shell script is executable."""
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_python_test_script_passes():
    """Verify that the student's test script runs successfully and exits with 0."""
    result = subprocess.run(
        ["python3", TEST_SCRIPT_PATH],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Student test script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_rate_limit_logic():
    """Verify the logic of rate_limit.sh using a hidden test set."""
    input_data = (
        "1620000000 192.168.1.1 /api/v1/users\n"
        "1620000000 192.168.1.1 /api/v1/data\n"
        "1620000000 192.168.1.1 /api/v1/settings\n"
        "1620000000 10.0.0.5 /about\n"
        "1620000001 192.168.1.1 /api/v1/users\n"
        "1620000001 192.168.1.1 /api/v1/users\n"
        "1620000001 192.168.1.1 /api/v1/users\n"
        "1620000001 10.0.0.5 /api/v1/test\n"
        "1620000001 10.0.0.5 /api/v1/test2\n"
        "1620000001 10.0.0.5 /api/v1/test3\n"
        "1620000002 10.0.0.5 /API/test\n"
        "1620000002 10.0.0.5 api/test\n"
    )

    expected_output = (
        "ALLOW 192.168.1.1 /api/v1/users\n"
        "ALLOW 192.168.1.1 /api/v1/data\n"
        "DENY 192.168.1.1 /api/v1/settings\n"
        "INVALID 10.0.0.5 /about\n"
        "ALLOW 192.168.1.1 /api/v1/users\n"
        "ALLOW 192.168.1.1 /api/v1/users\n"
        "DENY 192.168.1.1 /api/v1/users\n"
        "ALLOW 10.0.0.5 /api/v1/test\n"
        "ALLOW 10.0.0.5 /api/v1/test2\n"
        "DENY 10.0.0.5 /api/v1/test3\n"
        "INVALID 10.0.0.5 /API/test\n"
        "INVALID 10.0.0.5 api/test\n"
    )

    result = subprocess.run(
        [SCRIPT_PATH],
        input=input_data,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with exit code {result.returncode}."

    actual_output = result.stdout.strip()
    expected_output = expected_output.strip()

    assert actual_output == expected_output, (
        f"Script output did not match expected.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Got:\n{actual_output}"
    )