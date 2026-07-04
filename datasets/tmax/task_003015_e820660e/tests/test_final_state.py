# test_final_state.py

import os
import re
import pytest

APP_DIR = "/home/user/metrics_app"
HELPER_DIR = os.path.join(APP_DIR, "helper")
PROCESS_DATA_BIN = os.path.join(HELPER_DIR, "process_data")
DAEMON_FIXED_SCRIPT = os.path.join(APP_DIR, "daemon_fixed.sh")

def test_process_data_compiled():
    assert os.path.isfile(PROCESS_DATA_BIN), f"The binary {PROCESS_DATA_BIN} was not compiled or is missing."
    assert os.access(PROCESS_DATA_BIN, os.X_OK), f"The binary {PROCESS_DATA_BIN} is not executable."

def test_daemon_fixed_exists_and_executable():
    assert os.path.isfile(DAEMON_FIXED_SCRIPT), f"The fixed script {DAEMON_FIXED_SCRIPT} does not exist."
    assert os.access(DAEMON_FIXED_SCRIPT, os.X_OK), f"The fixed script {DAEMON_FIXED_SCRIPT} is not executable."

def test_daemon_fixed_auth_token():
    with open(DAEMON_FIXED_SCRIPT, 'r') as f:
        content = f.read()

    # Check if SUBMIT_TOKEN is set to ALPHA99
    assert "SUBMIT_TOKEN" in content, "The environment variable SUBMIT_TOKEN is missing in daemon_fixed.sh."
    assert "ALPHA99" in content, "The expected token value 'ALPHA99' is missing in daemon_fixed.sh."

def test_daemon_fixed_math_formula():
    with open(DAEMON_FIXED_SCRIPT, 'r') as f:
        content = f.read()

    # Check for proper grouping in arithmetic expansion, e.g., ((VAL1 + VAL2) / 2)
    # We look for parentheses around the addition before the division
    match = re.search(r'\(\s*\$?VAL1\s*\+\s*\$?VAL2\s*\)', content)
    assert match is not None, "The math formula in daemon_fixed.sh does not correctly group (VAL1 + VAL2) with parentheses."

def test_daemon_fixed_memory_leak():
    with open(DAEMON_FIXED_SCRIPT, 'r') as f:
        content = f.read()

    # The memory leak was caused by LOG_CACHE+=
    assert "LOG_CACHE+=" not in content, "The memory leak is not fixed: 'LOG_CACHE+=' is still present in daemon_fixed.sh."

    # Ensure it is now using assignment
    assert re.search(r'LOG_CACHE\s*=', content), "LOG_CACHE is not being assigned in daemon_fixed.sh."