# test_final_state.py

import os
import re
import subprocess
import pytest

SCRIPT_PATH = "/home/user/capacity_monitor.py"
LOG_PATH = "/home/user/memory_capacity.log"

def test_script_exists_and_executable():
    """Verify the script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_crontab_entry():
    """Verify the crontab contains the correct entry."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    # It's possible crontab is empty or returns an error if no crontab for user, but task requires it.
    assert result.returncode == 0, "Failed to read crontab. Ensure a crontab is set."

    crontab_content = result.stdout.strip().split('\n')
    found = False

    # Regex to match every minute cron expression and the specific command
    cron_regex = re.compile(r'^\s*\*\s+\*\s+\*\s+\*\s+\*\s+/usr/bin/python3\s+/home/user/capacity_monitor\.py\s*$')

    for line in crontab_content:
        # Ignore comments
        if line.strip().startswith('#'):
            continue
        if cron_regex.match(line):
            found = True
            break

    assert found, "Crontab does not contain the correct entry for every minute using /usr/bin/python3."

def test_script_execution_and_log_format():
    """Execute the script manually and verify the log format."""
    # Ensure script runs without error
    result = subprocess.run(['/usr/bin/python3', SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with output: {result.stderr}"

    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} was not created."

    with open(LOG_PATH, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"Log file {LOG_PATH} is empty."

    last_line = lines[-1].strip()

    # Format: YYYY-MM-DD HH:MM:SS | Used: XX.XX%
    log_regex = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| Used: \d+\.\d{2}%$')
    assert log_regex.match(last_line), f"Log entry format is incorrect. Got: '{last_line}'"

def test_error_handling_logic():
    """Check if the script contains the required error handling string."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    expected_error_msg = "ERROR: Cannot read meminfo"
    assert expected_error_msg in content, f"Script does not contain the expected error message: '{expected_error_msg}'"
    assert "try:" in content or "try " in content, "Script does not appear to use a try/except block for error handling."
    assert "except" in content, "Script does not appear to use a try/except block for error handling."