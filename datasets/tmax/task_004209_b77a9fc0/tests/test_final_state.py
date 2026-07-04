# test_final_state.py
import os
import re
import subprocess

def test_directory_and_symlink():
    log_dir = "/home/user/app_data/logs_v1"
    symlink = "/home/user/app_data/current_logs"

    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist."
    assert os.path.islink(symlink), f"{symlink} is not a symbolic link."

    target = os.readlink(symlink)
    # Both /home/user/app_data/logs_v1 and /home/user/app_data/logs_v1/ are acceptable
    assert target.rstrip('/') == log_dir, f"Symlink {symlink} points to {target}, expected {log_dir}"

def test_log_directory_size():
    log_dir = "/home/user/app_data/logs_v1"
    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist."

    total_size = sum(
        os.path.getsize(os.path.join(log_dir, f)) 
        for f in os.listdir(log_dir) 
        if os.path.isfile(os.path.join(log_dir, f))
    )

    assert total_size > 5 * 1024 * 1024, f"Total log size is {total_size} bytes, which is not strictly greater than 5MB."

def test_alert_log_content():
    alert_log = "/home/user/alerts.log"
    assert os.path.isfile(alert_log), f"Alert log {alert_log} does not exist."

    with open(alert_log, "r") as f:
        content = f.read().strip()

    pattern = r"^ALERT: Quota exceeded\. Rogue PID \d+ killed\.$"
    assert re.match(pattern, content), f"Alert log content '{content}' does not match expected format."

def test_processes_terminated():
    # Check if rogue_service.py is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "rogue_service.py"]).decode()
        pids = output.strip().split()
        assert not pids, f"rogue_service.py is still running with PIDs: {pids}"
    except subprocess.CalledProcessError:
        # pgrep returns 1 if no processes found, which is expected
        pass

    # Check if storage_monitor.py is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "storage_monitor.py"]).decode()
        pids = output.strip().split()
        assert not pids, f"storage_monitor.py is still running with PIDs: {pids}"
    except subprocess.CalledProcessError:
        pass