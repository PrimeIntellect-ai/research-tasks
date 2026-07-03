# test_final_state.py

import os
import pytest

def test_test_report_exists():
    """Verify that the test_report.log file was created."""
    log_path = '/home/user/test_report.log'
    assert os.path.exists(log_path), (
        f"The file {log_path} does not exist. Did you run the test_client.py script?"
    )
    assert os.path.isfile(log_path), (
        f"The path {log_path} exists but is not a file."
    )

def test_test_report_success_status():
    """Verify that the test_report.log file ends with the success status."""
    log_path = '/home/user/test_report.log'

    # Ensure the file exists before reading
    assert os.path.exists(log_path), f"Cannot check status, {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, f"The file {log_path} is empty."

    lines = content.split('\n')
    last_line = lines[-1]

    expected_status = "STATUS: ALL TESTS PASSED"

    assert last_line == expected_status, (
        f"Expected the last line of {log_path} to be '{expected_status}', "
        f"but got '{last_line}'. This indicates the test client failed one or more assertions."
    )