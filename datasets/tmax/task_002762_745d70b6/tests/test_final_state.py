# test_final_state.py

import os
import pytest

def test_found_errors_log_exists():
    """Check that the found_errors.log file exists."""
    log_path = "/home/user/found_errors.log"
    assert os.path.exists(log_path), f"The output log file was not found: {log_path}"
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

def test_found_errors_log_contents():
    """Check that the found_errors.log contains the exact expected lines."""
    log_path = "/home/user/found_errors.log"
    assert os.path.exists(log_path), f"The output log file was not found: {log_path}"

    expected_lines = [
        "bundle1.tar -> logsA.zip -> app2.txt: 2023-10-05 - ERROR_STATE_RACE_CONDITION in db_lock\n",
        "bundle2.tar -> logsB.zip -> app3.txt: 2023-10-06 - ERROR_STATE_RACE_CONDITION during cache flush\n"
    ]

    with open(log_path, 'r', encoding='utf-8') as f:
        actual_lines = f.readlines()

    # The task description requires the exact line including the newline, 
    # but some students might strip and re-add newlines. 
    # Let's ensure the content matches when stripped to be robust, 
    # but since the prompt says "including the newline", we check exact lines.

    expected_sorted = sorted(expected_lines)
    actual_sorted = sorted(actual_lines)

    assert actual_sorted == expected_sorted, (
        f"The contents of {log_path} do not match the expected output.\n"
        f"Expected:\n{expected_sorted}\n"
        f"Actual:\n{actual_sorted}"
    )

def test_script_exists():
    """Check that the script file was created."""
    script_path = "/home/user/scan_logs.py"
    assert os.path.exists(script_path), f"The script file was not found: {script_path}"
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."