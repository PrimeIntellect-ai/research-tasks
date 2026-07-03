# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

APP_DATA_DIR = "/home/user/app_data"
TRIGGER_SCRIPT = "/home/user/trigger_worker.sh"
MONITOR_SCRIPT = "/home/user/monitor.sh"
ALERT_LOG = "/home/user/alert.log"
HOME_DATA_LOG = "/home/user/data.log"
APP_DATA_LOG = "/home/user/app_data/data.log"

def test_app_data_directory_exists():
    assert os.path.isdir(APP_DATA_DIR), f"Directory {APP_DATA_DIR} does not exist."

def test_trigger_worker_exports_app_dir():
    assert os.path.isfile(TRIGGER_SCRIPT), f"{TRIGGER_SCRIPT} does not exist."
    with open(TRIGGER_SCRIPT, "r") as f:
        content = f.read()
    assert "APP_DIR=/home/user/app_data" in content, f"{TRIGGER_SCRIPT} does not set APP_DIR correctly."

def test_monitor_script_exists_and_executable():
    assert os.path.isfile(MONITOR_SCRIPT), f"{MONITOR_SCRIPT} does not exist."
    st = os.stat(MONITOR_SCRIPT)
    assert st.st_mode & stat.S_IXUSR, f"{MONITOR_SCRIPT} is not executable."

def test_trigger_worker_execution():
    # Clean up previous logs
    if os.path.exists(HOME_DATA_LOG):
        os.remove(HOME_DATA_LOG)
    if os.path.exists(APP_DATA_LOG):
        os.remove(APP_DATA_LOG)

    # Run the trigger script with stripped environment
    subprocess.run(["env", "-i", "bash", TRIGGER_SCRIPT], check=True)
    time.sleep(2)

    assert not os.path.exists(HOME_DATA_LOG), f"Data log should not be in /home/user/. Found {HOME_DATA_LOG}."
    assert os.path.exists(APP_DATA_LOG), f"Data log was not written to {APP_DATA_LOG}."

def test_monitor_script_under_quota():
    # Ensure size is under 1024
    if os.path.exists(os.path.join(APP_DATA_DIR, "large_file.dat")):
        os.remove(os.path.join(APP_DATA_DIR, "large_file.dat"))

    # Run monitor script
    subprocess.run(["bash", MONITOR_SCRIPT], check=True)

    assert os.path.isfile(ALERT_LOG), f"{ALERT_LOG} was not created."
    with open(ALERT_LOG, "r") as f:
        alert_content = f.read().strip()
    assert alert_content == "OK", f"Expected 'OK' in {ALERT_LOG}, got '{alert_content}'."

def test_monitor_script_over_quota():
    # Make sure the worker is running
    subprocess.run(["env", "-i", "bash", TRIGGER_SCRIPT], check=True)
    time.sleep(1)

    # Exceed quota
    large_file = os.path.join(APP_DATA_DIR, "large_file.dat")
    with open(large_file, "wb") as f:
        f.write(b"\0" * 2048)

    # Run monitor script
    subprocess.run(["bash", MONITOR_SCRIPT], check=True)

    # Check alert log
    assert os.path.isfile(ALERT_LOG), f"{ALERT_LOG} was not created."
    with open(ALERT_LOG, "r") as f:
        alert_content = f.read().strip()
    assert alert_content == "QUOTA EXCEEDED", f"Expected 'QUOTA EXCEEDED' in {ALERT_LOG}, got '{alert_content}'."

    # Check process was killed
    pgrep = subprocess.run(["pgrep", "-f", "service_worker"], capture_output=True)
    assert pgrep.returncode != 0, "service_worker process was not killed by monitor.sh."