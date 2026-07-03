# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_generate_report_script_exists():
    path = "/home/user/generate_report.py"
    assert os.path.isfile(path), f"Expected script {path} does not exist."

def test_summary_json_exists_and_permissions():
    path = "/home/user/reports/summary.json"
    assert os.path.isfile(path), f"Expected report file {path} does not exist."

    # Check permissions (0400)
    stat_info = os.stat(path)
    perms = stat_info.st_mode & 0o777
    assert perms == 0o400, f"Expected permissions 0400 for {path}, got {oct(perms)}"

def test_summary_json_content():
    aws_path = "/home/user/aws_cost.json"
    gcp_path = "/home/user/gcp_cost.json"
    summary_path = "/home/user/reports/summary.json"

    with open(aws_path, "r") as f:
        aws_cost = json.load(f)["cost"]
    with open(gcp_path, "r") as f:
        gcp_cost = json.load(f)["cost"]

    expected_sum = aws_cost + gcp_cost

    with open(summary_path, "r") as f:
        summary_data = json.load(f)

    assert "total_cost" in summary_data, "Key 'total_cost' missing in summary.json"
    assert summary_data["total_cost"] == expected_sum, f"Expected total_cost {expected_sum}, got {summary_data['total_cost']}"

def test_server_pid_running():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} from {pid_file} is not running."

def test_tunnel_pid_running():
    pid_file = "/home/user/tunnel.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} from {pid_file} is not running."

def test_port_forwarding():
    url = "http://127.0.0.1:9090/summary.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            assert "total_cost" in data, "Response JSON missing 'total_cost' key."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url} or retrieve summary.json: {e}"
    except json.JSONDecodeError:
        assert False, f"Failed to parse JSON from {url}."