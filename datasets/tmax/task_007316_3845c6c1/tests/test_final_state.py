# test_final_state.py

import os
import subprocess
import pytest

def test_rolling_loads_csv():
    """Verify the output CSV file is correct."""
    csv_path = "/home/user/output/rolling_loads.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    expected_csv = [
        "ts,server,rolling_load",
        "1,srv_alpha,2.0",
        "1,srv_beta,4.0",
        "2,srv_alpha,3.0",
        "2,srv_beta,5.0",
        "3,srv_alpha,5.0",
        "3,srv_beta,4.0",
        "4,srv_alpha,3.5",
        "4,srv_beta,5.0"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_csv, "The contents of rolling_loads.csv do not match the expected output."

def test_scripts_exist_and_executable():
    """Verify process.sh and setup_cron.sh exist and are executable."""
    process_sh = "/home/user/process.sh"
    setup_cron_sh = "/home/user/setup_cron.sh"

    assert os.path.isfile(process_sh), f"Script {process_sh} does not exist."
    assert os.access(process_sh, os.X_OK), f"Script {process_sh} is not executable."

    assert os.path.isfile(setup_cron_sh), f"Script {setup_cron_sh} does not exist."
    assert os.access(setup_cron_sh, os.X_OK), f"Script {setup_cron_sh} is not executable."

def test_cron_setup():
    """Verify setup_cron.sh correctly sets up the crontab."""
    setup_cron_sh = "/home/user/setup_cron.sh"

    # Run the setup script as the user (or current user)
    result = subprocess.run([setup_cron_sh], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {setup_cron_sh} failed."

    # Check crontab
    crontab_result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert crontab_result.returncode == 0, "Failed to read crontab."

    cron_lines = crontab_result.stdout.strip().split("\n")
    expected_cron = "0 * * * * /home/user/process.sh"

    # Check if any line in crontab matches the expected cron job (ignoring extra whitespace)
    found = False
    for line in cron_lines:
        # Normalize whitespace
        normalized_line = " ".join(line.strip().split())
        if expected_cron in normalized_line:
            found = True
            break

    assert found, f"Crontab does not contain the expected entry: '{expected_cron}'. Current crontab:\n{crontab_result.stdout}"