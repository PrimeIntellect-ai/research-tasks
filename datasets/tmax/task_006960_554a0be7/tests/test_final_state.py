# test_final_state.py

import os
import subprocess
import tarfile
import time

def test_bashrc_updated():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "export MONITOR_MODE=automated" in content, "The environment variable MONITOR_MODE was not exported in .bashrc"

def test_script_exists():
    script_path = "/home/user/service_monitor.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"

def test_script_missing_env_var():
    script_path = "/home/user/service_monitor.py"
    env = os.environ.copy()
    if "MONITOR_TARGET_PID" in env:
        del env["MONITOR_TARGET_PID"]

    result = subprocess.run(["python3", script_path], env=env)
    assert result.returncode == 1, "Script should exit with code 1 when MONITOR_TARGET_PID is missing"

def test_script_running_process():
    script_path = "/home/user/service_monitor.py"
    log_path = "/home/user/monitor.log"

    # Start a dummy process
    dummy_proc = subprocess.Popen(["sleep", "10"])

    env = os.environ.copy()
    env["MONITOR_TARGET_PID"] = str(dummy_proc.pid)

    try:
        result = subprocess.run(["python3", script_path], env=env)
        assert result.returncode == 0, "Script should exit with code 0 when process is running"

        assert os.path.isfile(log_path), f"Log file {log_path} was not created"
        with open(log_path, "r") as f:
            lines = f.readlines()
        assert any("[OK] Service running." in line for line in lines), "Success message not found in monitor.log"
    finally:
        dummy_proc.terminate()
        dummy_proc.wait()

def test_script_dead_process():
    script_path = "/home/user/service_monitor.py"
    log_path = "/home/user/monitor.log"
    backup_path = "/home/user/backup.tar.gz"

    # Remove existing backup if any
    if os.path.exists(backup_path):
        os.remove(backup_path)

    env = os.environ.copy()
    env["MONITOR_TARGET_PID"] = "999999"  # Unlikely to exist

    result = subprocess.run(["python3", script_path], env=env)
    assert result.returncode == 0, "Script should exit with code 0 when process is dead"

    assert os.path.isfile(log_path), f"Log file {log_path} was not created"
    with open(log_path, "r") as f:
        lines = f.readlines()
    assert any("[CRITICAL] Service down. Backup created." in line for line in lines), "Critical message not found in monitor.log"

    assert os.path.isfile(backup_path), f"Backup file {backup_path} was not created"

    # Verify backup contents
    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()
        # Check if data1.txt and data2.txt are in the tarball
        assert any("data1.txt" in name for name in names), "data1.txt not found in backup tarball"
        assert any("data2.txt" in name for name in names), "data2.txt not found in backup tarball"