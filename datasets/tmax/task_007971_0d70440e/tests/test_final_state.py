# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    """Verify that the script was created and is executable."""
    script_path = "/home/user/analyze_backups.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_csv_output_exists():
    """Verify that the output CSV file exists."""
    csv_path = "/home/user/restore_chain.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

def test_csv_output_content():
    """Verify that the output CSV file contains the correct restoration chain and cumulative sizes."""
    csv_path = "/home/user/restore_chain.csv"

    expected_lines = [
        "job_id,type,cumulative_size_bytes",
        "j002,full,10000",
        "j003,incremental,10500",
        "j006,incremental,10700",
        "j007,incremental,11000"
    ]

    with open(csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {csv_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )