# test_final_state.py

import os
import subprocess
import configparser
import pytest

def test_go_files_exist():
    go_src = "/home/user/net_troubleshooter.go"
    go_bin = "/home/user/net_troubleshooter"

    assert os.path.isfile(go_src), f"Go source file missing: {go_src}"
    assert os.path.isfile(go_bin), f"Compiled Go binary missing: {go_bin}"
    assert os.access(go_bin, os.X_OK), f"Go binary is not executable: {go_bin}"

def test_go_program_execution_and_output():
    go_bin = "/home/user/net_troubleshooter"
    alert_file = "/home/user/mailspool/alert.eml"

    # Remove alert file if it exists to ensure the program creates it
    if os.path.exists(alert_file):
        os.remove(alert_file)

    # Run the compiled binary
    result = subprocess.run([go_bin], capture_output=True)

    # Check exit code
    assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}"

    # Check alert file creation and contents
    assert os.path.isfile(alert_file), f"Alert file was not created at {alert_file}"

    with open(alert_file, "r") as f:
        content = f.read().strip()

    expected_content = """To: admin@local
Subject: Network Alert

Connection lost 3 times.
VNC Port: 5907"""

    assert content == expected_content, f"Alert file content does not match expected format.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_systemd_service_file():
    service_file = "/home/user/.config/systemd/user/net-watcher.service"
    assert os.path.isfile(service_file), f"Systemd service file missing: {service_file}"

    # Read the file
    with open(service_file, "r") as f:
        content = f.read()

    # Basic checks for required directives since configparser might struggle with systemd syntax without sections
    assert "ExecStart=/home/user/net_troubleshooter" in content, "Missing or incorrect ExecStart directive"
    assert "Restart=on-failure" in content, "Missing or incorrect Restart directive"
    assert "RestartSec=5" in content, "Missing or incorrect RestartSec directive"
    assert "WantedBy=default.target" in content, "Missing or incorrect WantedBy directive"