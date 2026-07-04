# test_final_state.py
import os
import re
import pytest

def test_run_telemetry_sh_modified():
    path = "/home/user/run_telemetry.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert 'HOME="/home/user"' in content or "HOME=/home/user" in content, \
        f"{path} does not set HOME to /home/user."

    assert "/sbin" in content and "/usr/sbin" in content, \
        f"{path} does not include /sbin and /usr/sbin in PATH."

def test_collect_sh_unmodified():
    path = "/home/user/collect.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert 'mkdir -p "$HOME/logs"' in content, f"{path} was modified."
    assert 'echo "Telemetry collected at $(date)"' in content, f"{path} was modified."

def test_telemetry_log_exists_and_successful():
    path = "/home/user/logs/telemetry.log"
    # Also check if it was rotated, but at least one log should exist or logrotate state should be updated
    # The instructions say "manually test the logrotate config", which might rename it to telemetry.log.1.gz
    # Let's check if the directory exists and has some log files
    log_dir = "/home/user/logs"
    assert os.path.isdir(log_dir), f"{log_dir} directory is missing."

    # Check if any telemetry log exists (could be rotated)
    log_files = [f for f in os.listdir(log_dir) if "telemetry.log" in f]
    assert len(log_files) > 0, "No telemetry.log found in /home/user/logs/."

    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
        assert "Network command failed" not in content, \
            "telemetry.log contains 'Network command failed', meaning PATH was not fixed correctly."

def test_extract_routes_sh_exists():
    path = "/home/user/extract_routes.sh"
    assert os.path.isfile(path), f"{path} is missing."

def test_routes_txt_correct():
    path = "/home/user/routes.txt"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["eth0:10.0.0.1", "wlan0:172.16.0.1"]
    assert lines == expected, f"{path} does not contain the correct routes. Expected {expected}, got {lines}."

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/logs/telemetry.log" in content, "logrotate.conf does not target /home/user/logs/telemetry.log"

    # Check for directives
    directives = ["daily", "rotate 4", "compress", "missingok"]
    for d in directives:
        # Use regex to allow for whitespace variations
        pattern = re.compile(r'\b' + d.replace(' ', r'\s+') + r'\b')
        assert pattern.search(content), f"logrotate.conf is missing directive: {d}"

def test_logrotate_state():
    path = "/home/user/logrotate.state"
    assert os.path.isfile(path), f"logrotate was not run manually as requested (missing {path})."