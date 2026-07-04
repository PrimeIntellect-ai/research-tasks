# test_final_state.py

import os
import stat
import subprocess
import hashlib
import pytest

SCRIPT_PATH = "/home/user/process_errors.sh"
UNIQUE_ERRORS_PATH = "/home/user/unique_errors.txt"
HASHES_PATH = "/home/user/processed_hashes.log"

EXPECTED_ERRORS = [
    "ERROR_CODE:500 MESSAGE:Internal Server Error",
    "ERROR_CODE:404 MESSAGE:Not Found",
    "ERROR_CODE:403 MESSAGE:Forbidden Access"
]

def test_script_exists_and_executable():
    """Verify that the process_errors.sh script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the user."

def test_crontab_configured():
    """Verify that the crontab is configured correctly."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured?")

    expected_cron = f"0 * * * * {SCRIPT_PATH}"
    # Check if the expected cron job is in the crontab output (ignoring leading/trailing whitespace)
    cron_lines = [line.strip() for line in crontab_content.splitlines()]
    assert expected_cron in cron_lines, f"Crontab does not contain the expected entry: '{expected_cron}'"

def test_script_execution_and_output():
    """Run the script and verify the generated files and their contents."""
    # Run the script
    try:
        subprocess.run([SCRIPT_PATH], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {SCRIPT_PATH} failed with error:\n{e.stderr}")

    # Verify unique_errors.txt
    assert os.path.isfile(UNIQUE_ERRORS_PATH), f"File {UNIQUE_ERRORS_PATH} was not created."

    with open(UNIQUE_ERRORS_PATH, "r") as f:
        unique_errors_content = f.read().splitlines()

    assert len(unique_errors_content) == len(EXPECTED_ERRORS), \
        f"Expected exactly {len(EXPECTED_ERRORS)} unique errors, found {len(unique_errors_content)}."

    for error in EXPECTED_ERRORS:
        assert error in unique_errors_content, f"Expected error '{error}' not found in {UNIQUE_ERRORS_PATH}."

    # Verify processed_hashes.log
    assert os.path.isfile(HASHES_PATH), f"File {HASHES_PATH} was not created."

    with open(HASHES_PATH, "r") as f:
        hashes_content = f.read().splitlines()

    assert len(hashes_content) == len(EXPECTED_ERRORS), \
        f"Expected exactly {len(EXPECTED_ERRORS)} hashes, found {len(hashes_content)}."

    # Compute expected hashes dynamically
    expected_hashes = [
        hashlib.sha256(error.encode('utf-8')).hexdigest()
        for error in EXPECTED_ERRORS
    ]

    for h in expected_hashes:
        assert h in hashes_content, f"Expected hash '{h}' not found in {HASHES_PATH}."