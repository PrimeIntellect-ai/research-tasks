# test_final_state.py

import os
import subprocess
import pytest

BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
SECRET_FILE = "/home/user/secret.txt"
FIXED_SCRIPT = "/home/user/fixed_calc.sh"
EXPECTED_BAD_COMMIT_FILE = "/tmp/expected_bad_commit.txt"
EXPECTED_SECRET = "B59x-L92Q-PZ11-M00X"

def test_bad_commit_txt():
    assert os.path.isfile(BAD_COMMIT_FILE), f"File {BAD_COMMIT_FILE} does not exist."
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"Truth file {EXPECTED_BAD_COMMIT_FILE} is missing."

    with open(BAD_COMMIT_FILE, "r") as f:
        actual_commit = f.read().strip()
    with open(EXPECTED_BAD_COMMIT_FILE, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {actual_commit}."

def test_secret_txt():
    assert os.path.isfile(SECRET_FILE), f"File {SECRET_FILE} does not exist."

    with open(SECRET_FILE, "r") as f:
        actual_secret = f.read().strip()

    assert actual_secret == EXPECTED_SECRET, f"Expected secret '{EXPECTED_SECRET}', but got '{actual_secret}'."

def test_fixed_calc_sh_exists_and_executable():
    assert os.path.isfile(FIXED_SCRIPT), f"Script {FIXED_SCRIPT} does not exist."
    assert os.access(FIXED_SCRIPT, os.X_OK), f"Script {FIXED_SCRIPT} is not executable."

def test_fixed_calc_sh_execution_100():
    try:
        result = subprocess.run(
            [FIXED_SCRIPT, "100"],
            capture_output=True,
            text=True,
            timeout=1.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {FIXED_SCRIPT} 100 timed out (infinite loop not fixed).")

    assert result.returncode == 0, f"Script exited with non-zero code: {result.returncode}"
    output = result.stdout.strip()
    assert output == "10", f"Expected output '10', but got '{output}'."

def test_fixed_calc_sh_execution_25():
    try:
        result = subprocess.run(
            [FIXED_SCRIPT, "25"],
            capture_output=True,
            text=True,
            timeout=1.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {FIXED_SCRIPT} 25 timed out (infinite loop not fixed).")

    assert result.returncode == 0, f"Script exited with non-zero code: {result.returncode}"
    output = result.stdout.strip()
    assert output == "5", f"Expected output '5', but got '{output}'."