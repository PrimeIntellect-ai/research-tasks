# test_final_state.py

import os
import re
import pytest

def test_monitor_routes_script_exists():
    path = "/home/user/monitor_routes.py"
    assert os.path.isfile(path), f"Expected script {path} does not exist."

def test_logrotate_conf_exists_and_configured():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"Expected config {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check for required directives. We use regex to allow formatting flexibility.
    assert re.search(r'\bsize\s+20\b', content), f"logrotate.conf missing 'size 20' directive."
    assert re.search(r'\brotate\s+3\b', content), f"logrotate.conf missing 'rotate 3' directive."
    assert re.search(r'\bcreate\b', content), f"logrotate.conf missing 'create' directive."
    assert re.search(r'\bnocompress\b', content), f"logrotate.conf missing 'nocompress' directive."

def test_logrotate_state_exists():
    path = "/home/user/lr.state"
    assert os.path.isfile(path), f"Expected logrotate state file {path} does not exist. Did you run logrotate with the custom state file?"

def test_logs_rotated_correctly():
    log_file = "/home/user/migration.log"
    log_1 = "/home/user/migration.log.1"
    log_2 = "/home/user/migration.log.2"

    assert os.path.isfile(log_file), f"{log_file} does not exist."
    assert os.path.isfile(log_1), f"{log_1} does not exist. Log rotation may not have run or failed."
    assert os.path.isfile(log_2), f"{log_2} does not exist. Log rotation may not have run twice as requested."

    # Check that the current log is empty (since it was just rotated and created)
    assert os.path.getsize(log_file) == 0, f"{log_file} should be 0 bytes after the second rotation."

    expected_content = "127.0.0.1 - STATUS: UP\n198.51.100.254 - STATUS: DOWN\n"

    for rotated_log in [log_1, log_2]:
        with open(rotated_log, "r") as f:
            content = f.read()

        # We allow some flexibility in whitespace, but the core strings must be present
        assert "127.0.0.1 - STATUS: UP" in content, f"{rotated_log} missing correct UP status for 127.0.0.1"
        assert "198.51.100.254 - STATUS: DOWN" in content, f"{rotated_log} missing correct DOWN status for 198.51.100.254"