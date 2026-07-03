# test_final_state.py

import os
import re
import pytest

def test_script_exists_and_executable():
    """Verify that the process_logs.sh script exists and is executable."""
    script_path = "/home/user/process_logs.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_output_csv_content():
    """Verify that the output CSV file is correctly formatted and aggregated."""
    output_file = "/home/user/output/max_memory.csv"
    assert os.path.exists(output_file), f"Output file missing: {output_file}"
    assert os.path.isfile(output_file), f"Path is not a file: {output_file}"

    expected_content = (
        "hour,hostname,max_value\n"
        "2023-10-12 08:00:00,server-a,2048\n"
        "2023-10-12 08:00:00,server-b,512\n"
        "2023-10-12 09:00:00,server-a,4096\n"
        "2023-10-12 09:00:00,server-b,8192\n"
    )

    with open(output_file, "r") as f:
        actual_content = f.read()

    # Normalize newlines and strip trailing whitespace
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, "Output CSV content does not match expected aggregated data."

def test_cron_backup():
    """Verify that the cron backup file exists and contains the correct cron job."""
    cron_file = "/home/user/cron_backup.txt"
    assert os.path.exists(cron_file), f"Cron backup file missing: {cron_file}"
    assert os.path.isfile(cron_file), f"Path is not a file: {cron_file}"

    with open(cron_file, "r") as f:
        cron_content = f.read()

    # Regex to match minute 0 of every hour running the script
    # Matches: 0 * * * * /home/user/process_logs.sh
    cron_pattern = re.compile(r"^0\s+\*\s+\*\s+\*\s+\*\s+/home/user/process_logs\.sh\b", re.MULTILINE)

    match = cron_pattern.search(cron_content)
    assert match is not None, f"Cron backup does not contain the correct schedule for /home/user/process_logs.sh at minute 0. Content:\n{cron_content}"