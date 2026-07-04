# test_final_state.py

import os
import pytest

WORKSPACE = "/home/user/deploy_check"
C_FILE = os.path.join(WORKSPACE, "deploy_validator.c")
BINARY = os.path.join(WORKSPACE, "deploy_validator")
SCRIPT = os.path.join(WORKSPACE, "run_tests.sh")
LOG_FILE = os.path.join(WORKSPACE, "validation_results.log")

def test_workspace_exists():
    assert os.path.isdir(WORKSPACE), f"Workspace directory {WORKSPACE} does not exist."

def test_c_source_exists():
    assert os.path.isfile(C_FILE), f"C source file {C_FILE} does not exist."

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY), f"Compiled binary {BINARY} does not exist."
    assert os.access(BINARY, os.X_OK), f"Compiled binary {BINARY} is not executable."

def test_script_exists():
    assert os.path.isfile(SCRIPT), f"Test script {SCRIPT} does not exist."

def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

def test_log_file_contents():
    expected_lines = [
        "DENY: Invalid token",
        "DENY: Hash mismatch",
        "DENY: Malicious payload",
        "ALLOW"
    ]

    with open(LOG_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in {LOG_FILE}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."