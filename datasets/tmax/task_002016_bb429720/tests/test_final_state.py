# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/generate_alerts.py"
LOG_PATH = "/home/user/fw_logs.txt"
ALERTS_PATH = "/home/user/alerts.txt"

def test_script_exists():
    """Check if the student created the required Python script."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_alerts_generated_correctly():
    """Check if alerts.txt contains the correct unique IP addresses sorted alphabetically."""
    assert os.path.isfile(ALERTS_PATH), f"Alerts file not found at {ALERTS_PATH}"

    with open(ALERTS_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = ["10.0.0.7", "10.1.1.1", "192.168.1.100"]

    assert lines == expected_ips, (
        f"Contents of {ALERTS_PATH} are incorrect. "
        f"Expected {expected_ips}, but got {lines}."
    )

def test_script_robustness_missing_log():
    """Check if the script handles a missing log file gracefully."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    # Temporarily hide the log file
    backup_path = "/home/user/fw_logs.txt.bak"
    if os.path.isfile(LOG_PATH):
        os.rename(LOG_PATH, backup_path)

    try:
        # Run the script
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True
        )

        # Check exit code
        assert result.returncode == 0, (
            f"Script crashed or returned non-zero exit code ({result.returncode}) "
            f"when {LOG_PATH} was missing. Stderr: {result.stderr}"
        )

        # Check that alerts.txt is created and empty
        assert os.path.isfile(ALERTS_PATH), f"Script did not create {ALERTS_PATH} when log file was missing."
        assert os.path.getsize(ALERTS_PATH) == 0, f"{ALERTS_PATH} should be empty when log file is missing."

    finally:
        # Restore the log file
        if os.path.isfile(backup_path):
            os.rename(backup_path, LOG_PATH)