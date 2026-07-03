# test_final_state.py

import os
import re
import subprocess
import pytest

def test_executable_exists_and_is_executable():
    exe_path = "/home/user/finops_monitor"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cost_alerts_log_content():
    log_path = "/home/user/cost_alerts.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "ALERT: volume vol_db_main exceeds 100",
        "ALERT: volume vol_analytics exceeds 100"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == 2, f"Expected exactly 2 alert lines, found {len(actual_lines)}."
    for expected in expected_lines:
        assert expected in actual_lines, f"Missing expected log entry: '{expected}'"

def test_crontab_entry_exists():
    try:
        # Try checking for the 'user' crontab specifically
        result = subprocess.run(['crontab', '-u', 'user', '-l'], capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback to current user
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    except Exception as e:
        pytest.fail(f"Failed to execute crontab command: {e}")

    assert result.returncode == 0, "Failed to retrieve crontab. Is it installed?"

    crontab_output = result.stdout

    # Match */5 * * * * /home/user/finops_monitor with flexible whitespace
    pattern = r"\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/finops_monitor"
    match = re.search(pattern, crontab_output)

    assert match is not None, "Crontab entry for /home/user/finops_monitor running every 5 minutes was not found."