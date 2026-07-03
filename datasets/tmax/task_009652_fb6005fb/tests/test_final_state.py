# test_final_state.py

import os
import re
import pytest

def test_config_file_contents():
    config_path = "/home/user/.config/finops/supervisor.conf"
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    # Check for required configuration settings
    assert 'TARGET_CMD="/home/user/cost_analyzer.py"' in content, "TARGET_CMD is missing or incorrect in config."
    assert 'HEARTBEAT_FILE="/home/user/heartbeat.txt"' in content, "HEARTBEAT_FILE is missing or incorrect in config."
    assert 'LOG_FILE="/home/user/supervisor.log"' in content, "LOG_FILE is missing or incorrect in config."

    # MAX_RESTARTS might be quoted or unquoted
    assert 'MAX_RESTARTS=3' in content or 'MAX_RESTARTS="3"' in content, "MAX_RESTARTS is missing or incorrect in config."

def test_supervisor_script_exists_and_executable():
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"Supervisor script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Supervisor script {script_path} is not executable."

def test_supervisor_log_contents():
    log_path = "/home/user/supervisor.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the supervisor run and create it?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in the log file, but found {len(lines)}."

    restart_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Restarted target process$")
    exit_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Max restarts reached, exiting$")

    for i in range(3):
        assert restart_pattern.match(lines[i]), f"Log line {i+1} does not match the expected restart format. Got: '{lines[i]}'"

    assert exit_pattern.match(lines[3]), f"Log line 4 does not match the expected exit format. Got: '{lines[3]}'"