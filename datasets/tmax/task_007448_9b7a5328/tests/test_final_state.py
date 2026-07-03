# test_final_state.py

import os
import gzip
import pytest

SCRIPT_PATH = "/home/user/project/process_logs.sh"
OUTPUT_PATH = "/home/user/project/error_logs.csv.gz"

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_output_file_exists():
    """Check if the output gzip file exists."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_file_contents():
    """Check if the output gzip file contains the correct filtered CSV data."""
    expected_lines = [
        '"2023-10-01T10:05:00Z","db","Connection timeout"',
        '"2023-10-01T10:10:00Z","auth","Invalid credentials provided"'
    ]

    try:
        with gzip.open(OUTPUT_PATH, 'rt', encoding='utf-8') as f:
            content = f.read().strip()
    except Exception as e:
        pytest.fail(f"Failed to read {OUTPUT_PATH} as a gzip file: {e}")

    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert sorted(actual_lines) == sorted(expected_lines), (
        "The contents of the error_logs.csv.gz do not match the expected CSV format or filtered records."
    )