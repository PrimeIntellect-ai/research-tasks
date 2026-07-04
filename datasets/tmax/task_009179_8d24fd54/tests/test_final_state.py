# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/process_metrics.sh"
CLEAN_METRICS_PATH = "/home/user/clean_metrics.csv"
SUMMARY_PATH = "/home/user/summary.txt"
CRON_SCHEDULE_PATH = "/home/user/cron_schedule"

EXPECTED_CLEAN_METRICS = [
    "S08,2023-10-01T11:55:00Z,21.0",
    "S01,2023-10-01T12:00:00Z,23.5",
    "S02,2023-10-01T12:05:00Z,24.1",
    "S03,2023-10-01T12:10:00Z,22.1",
    "S05,2023-10-01T12:15:00Z,19.5°C",
    "S07,2023-10-01T12:20:00Z,20.0"
]

EXPECTED_SUMMARY = "Processing complete. A total of 6 valid, unique time series points were extracted."

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_run_script_and_check_outputs():
    """Run the script and verify the generated files."""
    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. Stderr: {result.stderr}"

    # Check clean_metrics.csv
    assert os.path.isfile(CLEAN_METRICS_PATH), f"Output file {CLEAN_METRICS_PATH} was not created."
    with open(CLEAN_METRICS_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_CLEAN_METRICS, f"Contents of {CLEAN_METRICS_PATH} do not match expected output."

    # Check summary.txt
    assert os.path.isfile(SUMMARY_PATH), f"Summary file {SUMMARY_PATH} was not created."
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        summary_content = f.read().strip()

    assert summary_content == EXPECTED_SUMMARY, f"Contents of {SUMMARY_PATH} do not match expected output."

def test_cron_schedule():
    """Check if the cron schedule file exists and contains the correct entry."""
    assert os.path.isfile(CRON_SCHEDULE_PATH), f"Cron schedule file {CRON_SCHEDULE_PATH} does not exist."
    with open(CRON_SCHEDULE_PATH, "r", encoding="utf-8") as f:
        cron_content = f.read().strip()

    # Normalize spaces/tabs for comparison
    parts = cron_content.split()
    assert len(parts) >= 6, f"Cron schedule does not have enough fields: {cron_content}"

    expected_parts = ["15", "4", "*", "*", "2", SCRIPT_PATH]
    assert parts[:6] == expected_parts, f"Cron schedule entry is incorrect. Expected {expected_parts}, got {parts[:6]}"