# test_final_state.py

import os
import subprocess
import time
import pytest

def test_supervisor_script_exists_and_executable():
    script_path = "/home/user/supervisor.sh"
    assert os.path.exists(script_path), f"Supervisor script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_supervisor_execution_and_metric():
    # Clean up before running
    for f in ["/home/user/net.log", "/home/user/cache/data.bin"]:
        if os.path.exists(f):
            os.remove(f)

    script_path = "/home/user/supervisor.sh"

    # Run the supervisor script for 20 seconds
    try:
        proc = subprocess.Popen(
            ["bash", script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        time.sleep(20)
    finally:
        # Kill the supervisor and any child processes
        os.killpg(os.getpgid(proc.pid), 9)
        subprocess.run(["pkill", "-9", "net_worker"], capture_output=True)

    # Check config and backup files created by the script
    config_path = "/home/user/config.ini"
    backup_path = "/home/user/backups/config.ini.bak"

    assert os.path.exists(config_path), f"Config file {config_path} was not created."
    with open(config_path, "r") as f:
        assert "mode=active" in f.read(), f"Config file {config_path} does not contain 'mode=active'."

    assert os.path.exists(backup_path), f"Backup config file {backup_path} was not created."
    with open(backup_path, "r") as f:
        assert "mode=active" in f.read(), f"Backup config file {backup_path} does not contain 'mode=active'."

    # Check directories
    assert os.path.isdir("/home/user/cache"), "/home/user/cache directory does not exist."
    assert os.path.isdir("/home/user/backups"), "/home/user/backups directory does not exist."

    # Check the metric
    log_path = "/home/user/net.log"
    metric = 0
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            metric = sum(1 for line in f if "[PACKET_OK]" in line)

    threshold = 150
    assert metric >= threshold, f"Expected at least {threshold} [PACKET_OK] lines, but got {metric}. The daemon likely stalled or crashed without being restarted properly."