# test_final_state.py

import os
import json
import subprocess
import pytest

def test_summary_report_exists_and_correct():
    """Test that the summary report exists, is valid JSON, and has correct aggregations."""
    report_path = "/home/user/summary_report.json"
    assert os.path.isfile(report_path), f"Output file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    expected_data = {
        "NA": {
            "login": 1,
            "purchase": 1,
            "click": 1
        },
        "EU": {
            "login": 2,
            "purchase": 1
        }
    }

    assert data == expected_data, f"The contents of {report_path} do not match the expected aggregated statistics."

def test_run_pipeline_script_exists_and_executable():
    """Test that the run_pipeline.sh script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_crontab_configured_correctly():
    """Test that the crontab is configured to run the script at the top of every hour."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it installed for the current user?")

    cron_lines = [line.strip() for line in crontab_output.splitlines() if line.strip() and not line.startswith("#")]

    found = False
    for line in cron_lines:
        if "/home/user/run_pipeline.sh" in line:
            parts = line.split()
            if len(parts) >= 5:
                schedule = " ".join(parts[:5])
                if schedule == "0 * * * *":
                    found = True
                    break

    assert found, "Crontab does not contain the expected schedule '0 * * * *' for /home/user/run_pipeline.sh."