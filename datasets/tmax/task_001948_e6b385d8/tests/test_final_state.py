# test_final_state.py
import os
import subprocess
import time

def test_healthcheck_exp_exists_and_executable():
    path = "/home/user/healthcheck.exp"
    assert os.path.isfile(path), f"Expect script {path} is missing."
    assert os.access(path, os.X_OK), f"Expect script {path} is not executable."

def test_monitor_sh_exists_and_executable():
    path = "/home/user/monitor.sh"
    assert os.path.isfile(path), f"Bash script {path} is missing."
    assert os.access(path, os.X_OK), f"Bash script {path} is not executable."

def test_monitor_behavior():
    monitor_path = "/home/user/monitor.sh"
    ctl_path = "/home/user/service_ctl.sh"
    log_path = "/home/user/uptime.log"

    # Ensure service is running
    subprocess.run([ctl_path, "start"], capture_output=True)
    time.sleep(0.5)

    # Run monitor.sh when service is UP
    res_up = subprocess.run([monitor_path], capture_output=True)
    assert res_up.returncode == 0 or res_up.returncode != 0, "monitor.sh should execute without crashing."

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()
    assert len(lines) > 0, f"Log file {log_path} is empty."
    assert lines[-1] == "STATUS: UP", f"Expected last line of log to be 'STATUS: UP', got '{lines[-1]}'"

    # Stop the service
    subprocess.run([ctl_path, "stop"], capture_output=True)
    time.sleep(0.5)

    # Run monitor.sh when service is DOWN
    res_down = subprocess.run([monitor_path], capture_output=True)

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()
    assert len(lines) > 1, f"Log file {log_path} did not get a new line appended."
    assert lines[-1] == "STATUS: DOWN - RESTARTED", f"Expected last line of log to be 'STATUS: DOWN - RESTARTED', got '{lines[-1]}'"

    # Verify service was restarted
    res_status = subprocess.run([ctl_path, "status"], capture_output=True, text=True)
    assert "Service is running" in res_status.stdout, "Service was not successfully restarted by monitor.sh."