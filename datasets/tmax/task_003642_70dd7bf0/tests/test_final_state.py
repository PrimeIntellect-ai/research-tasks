# test_final_state.py

import os
import subprocess
import pytest

def test_metrics_csv_output():
    csv_path = "/home/user/output/metrics.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "timestamp,cpu_usage,rolling_avg",
        "1700000000,50.00,50.00",
        "1700000010,60.00,55.00",
        "1700000020,70.00,60.00",
        "1700000030,80.00,70.00",
        "1700000040,90.00,80.00"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_run_etl_sh_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_crontab_entry():
    # Try to get crontab for 'user', fallback to current user if it fails
    try:
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True)
        if result.returncode != 0:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    except Exception:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)

    crontab_output = result.stdout
    expected_cron = "*/15 * * * * /home/user/run_etl.sh"

    # Allow some flexibility in spacing
    found = False
    for line in crontab_output.splitlines():
        parts = line.split()
        if len(parts) >= 6 and parts[:5] == ["*/15", "*", "*", "*", "*"] and parts[5] == "/home/user/run_etl.sh":
            found = True
            break

    assert found, "Crontab entry '*/15 * * * * /home/user/run_etl.sh' not found."