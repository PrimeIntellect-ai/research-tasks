# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
SO_FILE = os.path.join(APP_DIR, "libbackend.so")
VALGRIND_LOG = os.path.join(APP_DIR, "valgrind_fixed.log")

def test_libbackend_compiled():
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} was not found. Did you compile it?"

def test_socat_running():
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command to check running processes.")

    socat_lines = [line for line in output.splitlines() if "socat" in line and "grep" not in line]
    assert socat_lines, "No socat process is running."

    # Check if socat is proxying port 8000 to 9000
    valid_proxy = False
    for line in socat_lines:
        if "8000" in line and "9000" in line:
            valid_proxy = True
            break

    assert valid_proxy, "socat is running, but doesn't seem to be configured to proxy port 8000 to 9000."

def test_valgrind_log_no_leaks():
    assert os.path.isfile(VALGRIND_LOG), f"Valgrind log {VALGRIND_LOG} was not found."

    with open(VALGRIND_LOG, "r") as f:
        content = f.read()

    assert "definitely lost: 0 bytes" in content, (
        "Memory leak is still present. 'definitely lost: 0 bytes' not found in valgrind log."
    )