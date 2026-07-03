# test_final_state.py

import os
import json
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    """
    Executes the student's script before running the tests to setup the final state.
    """
    script_path = "/home/user/start_observability.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out after 15 seconds. It may not be backgrounding processes correctly.")

def test_config_json_extracted():
    config_path = "/home/user/data/active/config.json"
    assert os.path.isfile(config_path), f"Expected config file at {config_path} is missing. Backup was not extracted properly."

def test_metrics_sock_created():
    sock_path = "/home/user/data/active/metrics.sock"
    assert os.path.isfile(sock_path), f"Expected socket file at {sock_path} is missing. metrics-gatherer.py may not have started successfully or was not waited on."

def test_pids_json_exists_and_valid():
    pids_path = "/home/user/run/pids.json"
    assert os.path.isfile(pids_path), f"Expected PIDs file at {pids_path} is missing."

    with open(pids_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {pids_path} does not contain valid JSON.")

    assert "gatherer_pid" in data, "Key 'gatherer_pid' is missing from pids.json."
    assert "backend_pid" in data, "Key 'backend_pid' is missing from pids.json."

    assert isinstance(data["gatherer_pid"], int), "Value for 'gatherer_pid' must be an integer."
    assert isinstance(data["backend_pid"], int), "Value for 'backend_pid' must be an integer."

def test_processes_running():
    pids_path = "/home/user/run/pids.json"

    # Skip if previous test failed to create valid JSON
    if not os.path.isfile(pids_path):
        pytest.skip("pids.json is missing.")

    with open(pids_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("pids.json is invalid.")

    gatherer_pid = data.get("gatherer_pid")
    backend_pid = data.get("backend_pid")

    if not isinstance(gatherer_pid, int) or not isinstance(backend_pid, int):
        pytest.skip("PIDs are not integers.")

    def get_cmdline(pid):
        try:
            with open(f"/proc/{pid}/cmdline", "r") as f:
                return f.read().replace('\x00', ' ').strip()
        except FileNotFoundError:
            return None

    gatherer_cmd = get_cmdline(gatherer_pid)
    assert gatherer_cmd is not None, f"Process with PID {gatherer_pid} (gatherer) is not running."
    assert "metrics-gatherer.py" in gatherer_cmd, f"PID {gatherer_pid} does not correspond to metrics-gatherer.py. Cmdline: {gatherer_cmd}"

    backend_cmd = get_cmdline(backend_pid)
    assert backend_cmd is not None, f"Process with PID {backend_pid} (backend) is not running."
    assert "dashboard-backend.py" in backend_cmd, f"PID {backend_pid} does not correspond to dashboard-backend.py. Cmdline: {backend_cmd}"