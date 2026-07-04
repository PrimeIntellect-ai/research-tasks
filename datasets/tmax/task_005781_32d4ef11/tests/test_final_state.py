# test_final_state.py

import os
import subprocess
import pytest

def test_etl_script_exists_and_executable():
    """Check if the ETL script exists and is executable."""
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"ETL script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"ETL script {script_path} is not executable."

def test_alerts_csv_content():
    """Check if alerts.csv contains the correct anomaly data."""
    alerts_path = "/home/user/alerts.csv"
    assert os.path.isfile(alerts_path), f"Alerts file {alerts_path} does not exist."

    with open(alerts_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2023-10-24T14,3",
        "2023-10-24T16,4"
    ]

    assert lines == expected_lines, f"Alerts file content is incorrect. Expected {expected_lines}, got {lines}."

def test_crontab_scheduled():
    """Check if the ETL script is scheduled in the crontab."""
    try:
        # Assuming the crontab is set for the 'user' user.
        # If running as root, we check the user's crontab.
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        try:
            # Fallback to current user if -u user fails
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            crontab_output = result.stdout
        except subprocess.CalledProcessError:
            pytest.fail("Failed to retrieve crontab. Is it set?")

    expected_cron_job = "15 * * * * /bin/bash /home/user/etl.sh"

    # Check if the expected cron job is in the crontab output, ignoring extra whitespace
    matching_lines = [
        line for line in crontab_output.splitlines()
        if "15" in line and "*" in line and "/bin/bash /home/user/etl.sh" in line
    ]

    assert matching_lines, f"Crontab does not contain the expected scheduled job: {expected_cron_job}"