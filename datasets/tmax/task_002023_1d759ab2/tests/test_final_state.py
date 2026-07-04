# test_final_state.py

import os
import subprocess
import pytest

KEY_FILE = "/home/user/key.txt"
VERIFY_SCRIPT = "/home/user/verify.py"
EXPECTED_KEY = "OpsFix99"

def test_key_file_exists_and_correct():
    """Test that the key file exists and contains the correct key."""
    assert os.path.exists(KEY_FILE), f"The file {KEY_FILE} does not exist."
    assert os.path.isfile(KEY_FILE), f"The path {KEY_FILE} is not a file."

    with open(KEY_FILE, "r") as f:
        content = f.read()

    assert content == EXPECTED_KEY, f"The file {KEY_FILE} does not contain the correct key. Expected '{EXPECTED_KEY}', got '{content}'."

def test_verify_script_exists_and_runs():
    """Test that verify.py exists and runs successfully."""
    assert os.path.exists(VERIFY_SCRIPT), f"The file {VERIFY_SCRIPT} does not exist."
    assert os.path.isfile(VERIFY_SCRIPT), f"The path {VERIFY_SCRIPT} is not a file."

    # Run the script and check exit code
    try:
        result = subprocess.run(
            ["python3", VERIFY_SCRIPT],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {VERIFY_SCRIPT} timed out.")

    assert result.returncode == 0, (
        f"Execution of {VERIFY_SCRIPT} failed with exit code {result.returncode}.\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )