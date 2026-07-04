# test_final_state.py

import os
import subprocess
import sys
import pytest

REPO_DIR = "/home/user/suspicious_tool"
TEST_FILE = "/home/user/test_c2_auth.py"
SECRET_TOKEN = "C2_TOK_77f9a2b4_exfiltrate"

def test_requirements_fixed_and_installable():
    req_path = os.path.join(REPO_DIR, "requirements.txt")
    assert os.path.isfile(req_path), f"File {req_path} does not exist."

    # Verify that pip can successfully resolve and install the requirements
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", req_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"Failed to install requirements.txt. The dependency conflict may still exist.\n"
        f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )

def test_test_file_exists_and_contains_secret():
    assert os.path.isfile(TEST_FILE), f"Test file {TEST_FILE} was not created."

    with open(TEST_FILE, "r") as f:
        content = f.read()

    assert SECRET_TOKEN in content, (
        f"The test file {TEST_FILE} does not contain the correct recovered secret token."
    )

def test_test_file_runs_successfully():
    assert os.path.isfile(TEST_FILE), f"Test file {TEST_FILE} is missing."

    env = os.environ.copy()
    # Ensure the malware module can be imported
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{REPO_DIR}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = REPO_DIR

    # Run pytest on the student's test file
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"pytest execution of {TEST_FILE} failed. Ensure the test is correctly written "
        f"and assertions pass.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )