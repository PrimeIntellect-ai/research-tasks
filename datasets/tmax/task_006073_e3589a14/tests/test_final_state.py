# test_final_state.py

import os
import subprocess
import time

def test_config_env():
    config_path = "/home/user/config.env"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read().strip()
    assert content == "STATUS=RUNNING", f"Expected STATUS=RUNNING in {config_path}, got {content}"

def test_heartbeat_c_exists():
    assert os.path.isfile("/home/user/heartbeat.c"), "/home/user/heartbeat.c does not exist."

def test_heartbeat_binary():
    binary_path = "/home/user/heartbeat"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_svc_sh_exists_and_executable():
    svc_path = "/home/user/svc.sh"
    assert os.path.isfile(svc_path), f"{svc_path} does not exist."
    assert os.access(svc_path, os.X_OK), f"{svc_path} is not executable."

def test_lifecycle():
    # Setup paths
    svc_path = "/home/user/svc.sh"
    log_path = "/home/user/heartbeat.log"
    pid_path = "/home/user/heartbeat.pid"

    # Clean up any existing logs or processes from previous runs
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(pid_path):
        try:
            with open(pid_path, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 9)
        except Exception:
            pass
        os.remove(pid_path)

    # 1. Test start
    result = subprocess.run([svc_path, "start"], capture_output=True, text=True)
    assert result.returncode == 0, f"svc.sh start failed with code {result.returncode}"
    time.sleep(1)

    assert os.path.isfile(pid_path), f"PID file {pid_path} was not created after start."
    with open(pid_path, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid PID: {pid_str}"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Daemon process with PID {pid} is not running."

    # 2. Test ping
    result = subprocess.run([svc_path, "ping"], capture_output=True, text=True)
    assert result.returncode == 0, f"svc.sh ping failed with code {result.returncode}"
    time.sleep(1)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        log_content = f.read()
    assert "Heartbeat received" in log_content, "SIGUSR1 not handled properly (missing 'Heartbeat received' in log)."

    # 3. Test stop
    result = subprocess.run([svc_path, "stop"], capture_output=True, text=True)
    assert result.returncode == 0, f"svc.sh stop failed with code {result.returncode}"
    time.sleep(1)

    # Check process terminated
    process_running = True
    try:
        os.kill(pid, 0)
    except OSError:
        process_running = False

    assert not process_running, f"Daemon process {pid} did not terminate after stop."
    assert not os.path.exists(pid_path), f"PID file {pid_path} was not removed after stop."

    with open(log_path, "r") as f:
        log_content = f.read()
    assert "Shutting down" in log_content, "SIGTERM not handled properly (missing 'Shutting down' in log)."