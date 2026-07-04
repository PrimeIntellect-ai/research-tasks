# test_final_state.py

import os
import subprocess
import re
import pytest

def test_c_program_exists_and_executable():
    source_file = "/home/user/etl_processor.c"
    executable_file = "/home/user/etl_processor"

    assert os.path.exists(source_file), f"Source file {source_file} does not exist."
    assert os.path.exists(executable_file), f"Executable file {executable_file} does not exist."
    assert os.access(executable_file, os.X_OK), f"File {executable_file} is not executable."

def test_etl_processor_output():
    executable_file = "/home/user/etl_processor"
    output_file = "/home/user/summary.csv"

    # Run the executable to ensure summary.csv is generated/updated
    try:
        subprocess.run([executable_file], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {executable_file} failed with error: {e.stderr}")

    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    expected_lines = [
        "2023-10-15T10:00:00Z,S01,21.00",
        "2023-10-15T10:00:00Z,S02,15.00",
        "2023-10-15T10:15:00Z,S01,26.00",
        "2023-10-15T10:30:00Z,S03,99.90",
        "2023-10-15T11:00:00Z,S01,50.00"
    ]

    with open(output_file, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."

def test_cron_job_configured():
    try:
        result = subprocess.run(["crontab", "-l"], check=True, capture_output=True, text=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab. Is it configured for the user?")

    # Check for the cron schedule and the executable path
    # Matches either '0,15,30,45 * * * *' or '*/15 * * * *' followed by the command
    pattern = re.compile(r'^((0,15,30,45|\*/15)\s+\*\s+\*\s+\*\s+\*)\s+(.*?)?/home/user/etl_processor', re.MULTILINE)

    match = pattern.search(crontab_content)
    assert match is not None, "Cron job for /home/user/etl_processor running every 15 minutes is not correctly configured."