# test_final_state.py

import os
import re
import pytest

def test_process_cpp_exists():
    """Test that the C++ program file exists."""
    assert os.path.isfile("/home/user/process.cpp"), "File /home/user/process.cpp does not exist."

def test_run_pipeline_sh_exists_and_executable():
    """Test that the shell script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_cron_txt_content():
    """Test that the cron.txt file contains the correct cron expression."""
    cron_path = "/home/user/cron.txt"
    assert os.path.isfile(cron_path), f"File {cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Valid minute fields: */15 or 0,15,30,45
    # The rest should be * * * *
    # Command should be /home/user/run_pipeline.sh
    # Example: */15 * * * * /home/user/run_pipeline.sh

    parts = content.split()
    assert len(parts) >= 6, "cron.txt does not contain a complete cron expression."

    minute_field = parts[0]
    assert minute_field in ("*/15", "0,15,30,45"), f"Invalid minute field in cron expression: {minute_field}. Expected '*/15' or '0,15,30,45'."

    assert parts[1:5] == ["*", "*", "*", "*"], "Cron expression should run every hour, day, month, and day of week (i.e. * * * *)."

    command = " ".join(parts[5:])
    assert command.endswith("/home/user/run_pipeline.sh") or "/home/user/run_pipeline.sh" in command, \
        f"Cron command does not seem to execute /home/user/run_pipeline.sh. Found: {command}"

def test_output_csv_content():
    """Test that the output.csv file exists and contains exactly the expected rolling averages."""
    output_path = "/home/user/output.csv"
    assert os.path.isfile(output_path), f"File {output_path} does not exist."

    expected_lines = [
        "2023-10-01 10:00:00,3.50",
        "2023-10-01 10:05:00,3.75",
        "2023-10-01 10:10:00,3.94",
        "2023-10-01 10:15:00,4.89",
        "2023-10-01 10:20:00,5.39"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.csv, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1} in output.csv. Expected: '{expected}', Actual: '{actual}'"