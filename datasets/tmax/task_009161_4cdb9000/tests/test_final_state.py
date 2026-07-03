# test_final_state.py

import os
import subprocess
import base64
import pytest

REPORT_PATH = "/home/user/uptime_report.txt"
SCRIPT_PATH = "/home/user/uptime_monitor.sh"
LOG_PATH = "/home/user/logs/ping_data.b64"

def test_uptime_report_exists():
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} does not exist. Did you run the script?"

def test_uptime_report_content():
    with open(REPORT_PATH, 'r') as f:
        content = f.read().strip()
    assert content == "Uptime: 75%", f"Expected 'Uptime: 75%', but got '{content}'"

def test_script_dynamic_calculation():
    # To ensure the user didn't hardcode "Uptime: 75%", we provide a new log file
    # with 2 successes and 2 failures -> 50% uptime
    new_log_data = b"1600000000,1\r\n1600000060,0\r\n1600000120,0\r\n1600000180,1\r\n"
    encoded_log = base64.b64encode(new_log_data)

    # Backup original log
    with open(LOG_PATH, 'rb') as f:
        original_log = f.read()

    try:
        # Write new log
        with open(LOG_PATH, 'wb') as f:
            f.write(encoded_log)

        # Run the script
        result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed to run with new data. stderr: {result.stderr}"

        # Check the report
        with open(REPORT_PATH, 'r') as f:
            content = f.read().strip()
        assert content == "Uptime: 50%", f"Script appears to have hardcoded output or failed to calculate correctly. Expected 'Uptime: 50%', got '{content}'"
    finally:
        # Restore original log and rerun script to restore state
        with open(LOG_PATH, 'wb') as f:
            f.write(original_log)
        subprocess.run([SCRIPT_PATH], capture_output=True)