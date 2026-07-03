# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
CPP_FILE = os.path.join(APP_DIR, "rotate_creds.cpp")
NEW_CREDS_FILE = os.path.join(APP_DIR, "new_creds.txt")
BINARY_FILE = os.path.join(APP_DIR, "rotate_creds")

def test_new_creds_content():
    assert os.path.isfile(NEW_CREDS_FILE), f"Expected output file {NEW_CREDS_FILE} does not exist."
    with open(NEW_CREDS_FILE, "r") as f:
        content = f.read().strip()
    assert content == "secR3t_k3Y_991_ROTATED", f"Incorrect credential derived. Found: {content}"

def test_seccomp_in_source():
    assert os.path.isfile(CPP_FILE), f"Source file {CPP_FILE} does not exist."
    with open(CPP_FILE, "r") as f:
        source_code = f.read()

    assert "SECCOMP_MODE_STRICT" in source_code, "Source code is missing SECCOMP_MODE_STRICT."
    assert "PR_SET_SECCOMP" in source_code, "Source code is missing PR_SET_SECCOMP."

def test_binary_exists_and_runs():
    assert os.path.isfile(BINARY_FILE), f"Compiled binary {BINARY_FILE} does not exist."
    assert os.access(BINARY_FILE, os.X_OK), f"Binary {BINARY_FILE} is not executable."

    # Run the binary to ensure it does not crash (e.g., from a seccomp violation)
    result = subprocess.run([BINARY_FILE], capture_output=True)
    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}. It may have crashed due to a seccomp violation."