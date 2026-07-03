# test_final_state.py

import os
import stat
import subprocess
import json
import time
import pytest

def test_setup_script_exists_and_executable():
    path = "/home/user/setup.sh"
    assert os.path.isfile(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_monitor_env_sh():
    path = "/home/user/monitor_env.sh"
    assert os.path.isfile(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "MONITOR_DIR=/home/user/data_drop" in content, "MONITOR_DIR not exported correctly"
    assert "SIZE_LIMIT=5000" in content, "SIZE_LIMIT not exported correctly"
    assert "ALERT_MAILBOX=/home/user/alerts.mbox" in content, "ALERT_MAILBOX not exported correctly"

def test_data_drop_directory():
    path = "/home/user/data_drop"
    assert os.path.isdir(path), f"{path} directory does not exist"

def test_register_exp():
    path = "/home/user/register.exp"
    assert os.path.isfile(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

    # Test if it runs successfully
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed to run"
    assert "Registration successful" in result.stdout, "Registration output incorrect"

def test_cron_job():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab"
    assert "monitor.py" in result.stdout, "monitor.py not found in crontab"
    assert "monitor_env.sh" in result.stdout, "monitor_env.sh not sourced in crontab"
    assert "* * * * *" in result.stdout, "Cron job not set to run every minute"

def test_monitor_py_functionality():
    monitor_script = "/home/user/monitor.py"
    data_dir = "/home/user/data_drop"
    mbox_file = "/home/user/alerts.mbox"
    state_file = "/home/user/monitor_state.json"

    assert os.path.isfile(monitor_script), f"{monitor_script} does not exist"
    assert os.access(monitor_script, os.X_OK), f"{monitor_script} is not executable"

    # Create a large file
    test_file = os.path.join(data_dir, "test_large_file.txt")
    with open(test_file, "wb") as f:
        f.write(b"0" * 6000)

    # Run the monitor script with the environment sourced
    run_cmd = f"source /home/user/monitor_env.sh && {monitor_script}"
    subprocess.run(["bash", "-c", run_cmd], check=True)

    # Check mbox
    assert os.path.isfile(mbox_file), f"{mbox_file} was not created"
    with open(mbox_file, "r") as f:
        mbox_content = f.read()

    assert "Subject: ALERT: Large file detected - test_large_file.txt" in mbox_content, "Alert email not found or subject incorrect"

    # Check state file
    assert os.path.isfile(state_file), f"{state_file} was not created"

    # Record mbox size
    mbox_size = os.path.getsize(mbox_file)

    # Run again
    subprocess.run(["bash", "-c", run_cmd], check=True)

    # Check that mbox size hasn't changed
    new_mbox_size = os.path.getsize(mbox_file)
    assert new_mbox_size == mbox_size, "Duplicate alert was generated"

    # Clean up test file
    os.remove(test_file)