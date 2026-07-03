# test_final_state.py

import os
import json
import subprocess

def test_log_file_and_json_content():
    log_path = "/home/user/dashboard_metrics.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected exactly 6 non-empty lines in {log_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {log_path} is not valid JSON: {line}"

        assert "directory" in data, f"'directory' key missing in JSON on line {i+1}."
        assert data["directory"] == "/home/user/app_data", f"Incorrect directory in JSON on line {i+1}."
        assert "available_bytes" in data, f"'available_bytes' key missing in JSON on line {i+1}."
        assert isinstance(data["available_bytes"], int), f"'available_bytes' is not an integer on line {i+1}."

def test_available_bytes_correct():
    log_path = "/home/user/dashboard_metrics.log"
    assert os.path.exists(log_path), "Log file missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "Log file is empty."
    data = json.loads(lines[0])
    reported_space = data["available_bytes"]

    # Calculate actual available space
    stat = os.statvfs("/home/user/app_data")
    actual_space = stat.f_bavail * stat.f_frsize

    # Allow a small delta (e.g., 50MB) for log file creation or minor filesystem changes
    delta = abs(reported_space - actual_space)
    assert delta < 50 * 1024 * 1024, f"Reported available space ({reported_space}) differs significantly from actual ({actual_space}). Bug in C++ code may not be correctly fixed."

def test_haproxy_running():
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to execute 'ps aux'."

    assert "haproxy" in output, "HAProxy process is not running."

def test_ssh_tunnel_running():
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to execute 'ps aux'."

    # Look for ssh command with port forwarding 9090
    ssh_running = any("ssh" in line and "9090" in line for line in output.splitlines())
    assert ssh_running, "SSH tunnel process for port 9090 is not running."

def test_backend_agents_running():
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to execute 'ps aux'."

    agent_lines = [line for line in output.splitlines() if "metrics_agent" in line and not "grep" in line]
    assert len(agent_lines) >= 3, "Expected at least 3 instances of metrics_agent running."

def test_poll_metrics_script_exists():
    script_path = "/home/user/poll_metrics.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Script {script_path} is not readable/executable."

def test_haproxy_cfg_exists():
    cfg_path = "/home/user/haproxy.cfg"
    assert os.path.exists(cfg_path), f"HAProxy config {cfg_path} is missing."