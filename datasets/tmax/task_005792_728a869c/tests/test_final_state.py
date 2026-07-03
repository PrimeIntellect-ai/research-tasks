# test_final_state.py

import os
import re
import pytest

def test_scripts_exist_and_executable():
    """Check if process.py and pipeline.sh exist and are executable."""
    scripts = [
        "/home/user/process.py",
        "/home/user/pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} is missing."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_cron_job_configuration():
    """Check if pipeline_cron contains the correct schedule."""
    cron_file = "/home/user/pipeline_cron"
    assert os.path.isfile(cron_file), f"Cron configuration file {cron_file} is missing."

    with open(cron_file, "r") as f:
        content = f.read().strip()

    # Look for the required schedule "30 2 * * *" and the script path
    assert "30 2 * * *" in content, f"Cron schedule '30 2 * * *' not found in {cron_file}."
    assert "/home/user/pipeline.sh" in content, f"Script path '/home/user/pipeline.sh' not found in {cron_file}."

def test_timeseries_csv_content():
    """Check if timeseries.csv exists and contains the correct sorted data."""
    csv_file = "/home/user/data/timeseries.csv"
    assert os.path.isfile(csv_file), f"Output file {csv_file} is missing."

    with open(csv_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "timestamp,value",
        "2023-10-01 10:00:00,15.2",
        "2023-10-02 10:00:00,16.8",
        "2023-10-03 10:00:00,14.9"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_file}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."