# test_final_state.py
import os
import urllib.request
import urllib.error

def test_bashrc_contains_env_vars():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "EDGE_DEVICE_ID=edge-node-42" in content, "EDGE_DEVICE_ID=edge-node-42 not found in .bashrc"
    assert "EDGE_PORT=8484" in content, "EDGE_PORT=8484 not found in .bashrc"

def test_bare_git_repo_exists():
    git_dir = "/home/user/iot-hub.git"
    assert os.path.isdir(git_dir), f"{git_dir} directory does not exist."
    config_path = os.path.join(git_dir, "config")
    assert os.path.isfile(config_path), f"Git config not found at {config_path}. Is it a valid bare repo?"
    with open(config_path, "r") as f:
        content = f.read()
    assert "bare = true" in content.lower(), "Repository is not configured as bare."

def test_deployment_log_success():
    log_path = "/home/user/deployment_log.txt"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "[edge-node-42] DEPLOYMENT_SUCCESS" in content, "Deployment success message not found in log."

def test_http_server_ping():
    url = "http://127.0.0.1:8484/ping"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode("utf-8").strip()
            assert body == "pong", f"Expected body 'pong', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url}: {e}"

def test_pid_file_and_process():
    pid_file = "/home/user/edge_service.pid"
    assert os.path.isfile(pid_file), f"{pid_file} does not exist."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."