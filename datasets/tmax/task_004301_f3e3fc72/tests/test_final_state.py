# test_final_state.py

import os
import json
import stat
import subprocess
import time

def test_backup_created():
    """Check that the backup file exists and contains the original wrong socket path."""
    backup_path = "/home/user/backups/config.json.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    with open(backup_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Backup file {backup_path} is not valid JSON."

    assert config.get("upstream_socket") == "/tmp/wrong_app.sock", \
        "Backup file does not contain the original 'upstream_socket' value."

def test_bash_profile_updated():
    """Check that .bash_profile contains the correct export statement."""
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"Profile file {profile_path} is missing."

    with open(profile_path, "r") as f:
        content = f.read()

    expected_line = "export APP_SOCKET_PATH=/home/user/appstack/run/app.sock"
    assert expected_line in content, \
        f"{profile_path} does not contain the expected export statement."

def test_config_updated():
    """Check that config.json has been updated with the correct socket path."""
    config_path = "/home/user/appstack/config.json"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Config file {config_path} is not valid JSON."

    assert config.get("upstream_socket") == "/home/user/appstack/run/app.sock", \
        "config.json 'upstream_socket' was not updated to the correct path."

def test_final_output_log():
    """Check that the final_output.log contains the exact expected output."""
    log_path = "/home/user/final_output.log"
    assert os.path.isfile(log_path), f"Final output log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_output = '{"status": "healthy", "component": "backend"}'
    assert content == expected_output, \
        f"Output log content is incorrect. Expected '{expected_output}', got '{content}'."

def test_manager_script_lifecycle():
    """Test the manager.sh script for start and stop functionality."""
    manager_path = "/home/user/appstack/manager.sh"
    backend_pid_file = "/home/user/appstack/run/backend.pid"
    proxy_pid_file = "/home/user/appstack/run/proxy.pid"

    assert os.path.isfile(manager_path), f"Manager script {manager_path} is missing."
    st = os.stat(manager_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Manager script {manager_path} is not executable."

    # Clear state
    subprocess.run(["killall", "python3", "socat"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if os.path.exists(backend_pid_file):
        os.remove(backend_pid_file)
    if os.path.exists(proxy_pid_file):
        os.remove(proxy_pid_file)

    # Test start
    subprocess.run(["/bin/bash", manager_path, "start"], cwd="/home/user/appstack")
    time.sleep(2)

    assert os.path.isfile(backend_pid_file), f"Backend PID file {backend_pid_file} was not created after start."
    assert os.path.isfile(proxy_pid_file), f"Proxy PID file {proxy_pid_file} was not created after start."

    with open(backend_pid_file, "r") as f:
        backend_pid = f.read().strip()
    with open(proxy_pid_file, "r") as f:
        proxy_pid = f.read().strip()

    assert backend_pid.isdigit(), "Backend PID file does not contain a valid PID."
    assert proxy_pid.isdigit(), "Proxy PID file does not contain a valid PID."

    # Verify processes are actually running
    def is_running(pid):
        try:
            os.kill(int(pid), 0)
            return True
        except OSError:
            return False

    assert is_running(backend_pid), "Backend process is not running."
    assert is_running(proxy_pid), "Proxy process is not running."

    # Test stop
    subprocess.run(["/bin/bash", manager_path, "stop"], cwd="/home/user/appstack")
    time.sleep(2)

    assert not os.path.isfile(backend_pid_file), "Backend PID file was not removed after stop."
    assert not os.path.isfile(proxy_pid_file), "Proxy PID file was not removed after stop."

    assert not is_running(backend_pid), "Backend process was not terminated."
    assert not is_running(proxy_pid), "Proxy process was not terminated."