# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    """Test if the bash script exists and is executable."""
    script_path = "/home/user/build_and_test.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_executable_compiled():
    """Test if the C program was compiled to the correct location."""
    exe_path = "/home/user/bin/math_check"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"Compiled file {exe_path} is not executable."

def test_test_data_fixture():
    """Test if the test fixture file contains numbers 1 to 20."""
    data_path = "/home/user/test_data.txt"
    assert os.path.isfile(data_path), f"Test data file {data_path} does not exist."

    with open(data_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [str(i) for i in range(1, 21)]
    assert lines == expected_lines, f"Test data file {data_path} does not contain the expected integers 1 through 20."

def test_test_report_log():
    """Test if the test report log contains the correct PASS lines."""
    log_path = "/home/user/test_report.log"
    assert os.path.isfile(log_path), f"Test report log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [f"[{i}] PASS" for i in range(1, 21)]
    assert lines == expected_lines, f"Test report log {log_path} does not contain the expected PASS lines."