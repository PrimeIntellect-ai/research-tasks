# test_final_state.py

import os
import re
import subprocess
import urllib.request
import pytest

def test_uptime_monitor_running():
    """Verify that the uptime_monitor process is running."""
    try:
        output = subprocess.check_output(["ps", "-e", "-o", "command"], text=True)
        assert "uptime_monitor" in output, "uptime_monitor process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

def test_ssh_tunnel_running():
    """Verify that the SSH tunnel is listening on port 9090."""
    try:
        output = subprocess.check_output(["ss", "-tln"], text=True)
        assert ":9090" in output, "SSH tunnel is not listening on port 9090."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ss command.")

def test_result_txt():
    """Verify that result.txt contains the correct integer."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"{result_path} does not exist."
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content == "5", f"Expected '5' in {result_path}, got '{content}'."

def test_log_rotation_and_content():
    """Verify that logrotate created uptime.log.1 with correct JST timestamps."""
    log_file = "/home/user/app_logs/uptime.log.1"
    assert os.path.isfile(log_file), f"Rotated log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.readlines()

    jst_lines = [line for line in lines if "JST] SYSTEM_UP" in line]
    assert len(jst_lines) == 5, f"Expected exactly 5 'JST] SYSTEM_UP' lines in {log_file}, found {len(jst_lines)}."

    # Check the format of the timestamp
    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\] SYSTEM_UP\n$")
    for line in jst_lines:
        assert pattern.match(line), f"Log line format incorrect: {line}"

def test_logrotate_conf():
    """Verify the logrotate configuration file exists and has required directives."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "copytruncate" in content, "Missing 'copytruncate' in logrotate.conf."
    assert "10" in content, "Missing size directive (e.g. 'size 10') in logrotate.conf."
    assert "3" in content, "Missing rotate directive (e.g. 'rotate 3') in logrotate.conf."

def test_uptime_monitor_c_exists():
    """Verify the C source code file exists."""
    c_path = "/home/user/uptime_monitor.c"
    assert os.path.isfile(c_path), f"C source file {c_path} does not exist."

def test_service_response():
    """Verify the uptime service responds correctly via the SSH tunnel."""
    try:
        req = urllib.request.Request("http://127.0.0.1:9090")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8')
            assert body == "UPTIME_OK", f"Expected response 'UPTIME_OK', got '{body}'"
    except Exception as e:
        pytest.fail(f"Failed to connect to service via tunnel on port 9090: {e}")