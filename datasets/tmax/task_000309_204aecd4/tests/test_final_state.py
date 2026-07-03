# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/clean_and_correlate.sh"
CLEANED_CSV_PATH = "/home/user/cleaned_features.csv"
CORRELATION_TXT_PATH = "/home/user/correlation.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable"

def test_script_execution_and_outputs():
    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Verify cleaned_features.csv
    assert os.path.isfile(CLEANED_CSV_PATH), f"Output file {CLEANED_CSV_PATH} was not created"

    with open(CLEANED_CSV_PATH, "r") as f:
        cleaned_lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "10.0,12.0",
        "25.0,22.0",
        "20.0,18.0",
        "30.0,28.0",
        "-10.0,-5.0",
        "5.0,8.0"
    ]

    assert sorted(cleaned_lines) == sorted(expected_lines), (
        f"Contents of {CLEANED_CSV_PATH} do not match expected pairs. "
        f"Expected: {sorted(expected_lines)}, Got: {sorted(cleaned_lines)}"
    )

    # Verify correlation.txt
    assert os.path.isfile(CORRELATION_TXT_PATH), f"Output file {CORRELATION_TXT_PATH} was not created"

    with open(CORRELATION_TXT_PATH, "r") as f:
        correlation_val = f.read().strip()

    assert correlation_val == "0.992", f"Correlation value incorrect. Expected '0.992', Got '{correlation_val}'"