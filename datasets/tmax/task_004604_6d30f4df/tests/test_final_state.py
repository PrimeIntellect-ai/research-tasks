# test_final_state.py

import os
import re
import subprocess
import pytest

LOG_FILE = "/home/user/deployment_final.log"
EXPECTED_PATHS = [
    "/home/user/run/microvm_alpha.sock",
    "/home/user/run/microvm_beta.sock",
    "/home/user/run/microvm_gamma.sock"
]

def test_log_file_exists_and_content():
    assert os.path.isfile(LOG_FILE), f"The log file {LOG_FILE} was not created."

    with open(LOG_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 log entries in {LOG_FILE}, found {len(lines)}."

    for i, expected_path in enumerate(EXPECTED_PATHS):
        line = lines[i]
        match = re.match(r"^DEPLOYED PID ([0-9]+) TO (.*)$", line)
        assert match, f"Log line {i+1} does not match expected format: {line}"

        pid_str, path = match.groups()
        assert path == expected_path, f"Expected path {expected_path} in log line {i+1}, found {path}"

        # Verify PID is a number
        assert pid_str.isdigit(), f"Extracted PID {pid_str} is not a valid number."

def test_processes_are_running():
    for expected_path in EXPECTED_PATHS:
        # We check if the process is running using pgrep
        cmd = ["pgrep", "-f", f"/home/user/bin/qemu_mock.sh {expected_path}"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0, f"Process for {expected_path} is not running."

        # Check if the socket file was actually created by the mock script
        assert os.path.exists(expected_path), f"Socket file {expected_path} was not created."

def test_deployment_script_modified():
    script_path = "/home/user/deploy_vms.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "/tmp/vm_1.sock" not in content, "The deployment script still contains hardcoded /tmp/ paths."
    assert "nginx.conf" in content or "grep" in content or "awk" in content or "sed" in content, \
        "The deployment script doesn't seem to parse nginx.conf or extract paths dynamically."