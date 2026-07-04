# test_final_state.py

import os
import json
import subprocess
import pytest

def test_analyze_logs_output():
    script_path = "/home/user/analyze_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed with return code {result.returncode}."

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert set(output_lines) == {"8002", "8003"}, f"Expected output to contain exactly '8002' and '8003', got {output_lines}"

def test_recovery_status_json():
    json_path = "/home/user/recovery_status.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "8002" in data, "Port '8002' missing from recovery_status.json."
    assert "8003" in data, "Port '8003' missing from recovery_status.json."
    assert "8001" not in data, "Port '8001' should not be in recovery_status.json."

    for port in ["8002", "8003"]:
        port_data = data[port]
        assert isinstance(port_data, dict), f"Data for port {port} is not a dictionary."
        assert port_data.get("status") == "recovered", f"Status for port {port} is not 'recovered'."
        assert "new_pid" in port_data, f"'new_pid' missing for port {port}."

        pid_file = f"/home/user/services/pids/{port}.pid"
        assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

        with open(pid_file, "r") as pf:
            pid_str = pf.read().strip()
            assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."
            actual_pid = int(pid_str)

        assert port_data["new_pid"] == actual_pid, f"new_pid for port {port} in JSON ({port_data['new_pid']}) does not match PID file ({actual_pid})."

def test_processes_running():
    for port in ["8001", "8002", "8003"]:
        pid_file = f"/home/user/services/pids/{port}.pid"
        assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

        with open(pid_file, "r") as pf:
            pid_str = pf.read().strip()
            assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."
            pid = int(pid_str)

        try:
            os.kill(pid, 0)
        except OSError:
            pytest.fail(f"Process with PID {pid} for port {port} is not running.")