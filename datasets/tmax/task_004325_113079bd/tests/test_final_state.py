# test_final_state.py

import os
import subprocess
import pytest

def test_nginx_config_fixed():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config {conf_path} is missing."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "unix:/home/user/app/backend.sock;" in content, "The Nginx configuration was not updated to point to the correct backend.sock path."
    assert "unix:/home/user/app/wrong.sock;" not in content, "The old wrong.sock path is still present in the Nginx configuration."

def test_script_exists_and_executable():
    script_path = "/home/user/alert_monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_output():
    script_path = "/home/user/alert_monitor.sh"
    log_path = "/home/user/nginx/logs/error.log"
    report_path = "/home/user/502_report.txt"

    # Remove report if it exists to ensure we are testing the script's current output
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the script
    result = subprocess.run([script_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. Error: {result.stderr}"

    assert os.path.isfile(report_path), f"Report file {report_path} was not created by the script."

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[2023/11/01 10:16:22] Client: 10.0.0.5 - Upstream: http://unix:/home/user/app/wrong.sock:/api",
        "[2023/11/01 10:18:45] Client: 172.16.0.12 - Upstream: http://unix:/home/user/app/wrong.sock:/login"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in report does not match expected format.\nExpected: {expected}\nGot: {lines[i]}"