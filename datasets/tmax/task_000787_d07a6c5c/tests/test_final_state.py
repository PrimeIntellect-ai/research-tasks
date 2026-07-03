# test_final_state.py

import os
import re

def test_bashrc_contains_export():
    """Check if MAX_STORAGE_MB is set to 40 and exported in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"File {bashrc_path} does not exist."

    with open(bashrc_path, 'r') as f:
        content = f.read()

    # Check for MAX_STORAGE_MB=40
    assert re.search(r'^[^#]*MAX_STORAGE_MB\s*=\s*"?40"?', content, re.MULTILINE), \
        "MAX_STORAGE_MB=40 is not set in .bashrc."

    # Check if it's exported
    assert re.search(r'^[^#]*export\s+.*MAX_STORAGE_MB', content, re.MULTILINE) or \
           re.search(r'^[^#]*export\s+MAX_STORAGE_MB\s*=\s*"?40"?', content, re.MULTILINE), \
        "MAX_STORAGE_MB is not exported in .bashrc."

def test_monitor_sh_executable():
    """Check if monitor.sh exists and is executable."""
    script_path = "/home/user/monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_health_log_contents():
    """Check if health.log contains the correct output based on the directory size."""
    log_path = "/home/user/health.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected_log = "CRITICAL: Storage at 45MB exceeds limit of 40MB"
    assert expected_log in content, \
        f"Expected log entry '{expected_log}' not found in {log_path}. Found:\n{content}"