# test_final_state.py

import os

def test_waf_server_compiled():
    """Check if the waf_server binary has been compiled successfully."""
    server_path = "/home/user/waf_pr/waf_server"
    assert os.path.isfile(server_path), f"The binary {server_path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(server_path, os.X_OK), f"The file {server_path} is not executable."

def test_results_log_correct():
    """Verify that results.log contains the correct output from the integration tests."""
    log_path = "/home/user/waf_pr/results.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist. Did you run the integration script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Test 1: BLOCK",
        'action": "BLOCK"',
        "Test 2: ALLOW",
        'action": "ALLOW"',
        "Test 3: CHALLENGE",
        'action": "CHALLENGE"'
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.log, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in results.log is incorrect. Expected '{expected}', got '{actual}'."