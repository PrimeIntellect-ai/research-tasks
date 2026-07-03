# test_final_state.py

import os
import stat
import subprocess
import time
import re

SCRIPT_PATH = "/home/user/ensure_service.sh"
MICROSERVICE_PATH = "/home/user/microservice.sh"
PID_FILE = "/home/user/service.pid"
LOG_FILE = "/home/user/watcher.log"

def kill_microservice():
    """Helper to kill any running microservice processes."""
    try:
        subprocess.run(["pkill", "-f", "microservice.sh"], check=False)
    except Exception:
        pass

def is_process_running(pid):
    """Check if a process with the given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def get_last_log_line():
    """Get the last line of the watcher log."""
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        if lines:
            return lines[-1].strip()
    return ""

def test_script_exists_and_executable():
    """Test that ensure_service.sh exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Expected script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Expected {SCRIPT_PATH} to be a file."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expected {SCRIPT_PATH} to be executable."

def test_crontab_scheduled():
    """Test that the script is scheduled in crontab to run every minute."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    found = False
    for line in result.stdout.splitlines():
        if line.strip().startswith("#"):
            continue
        if "ensure_service.sh" in line:
            # Check if it's scheduled every minute (* * * * *)
            parts = line.split()
            if len(parts) >= 5 and parts[:5] == ["*", "*", "*", "*", "*"]:
                found = True
                break

    assert found, "ensure_service.sh is not scheduled to run every minute (* * * * *) in crontab."

def test_script_behavior_started():
    """Test the STARTED state of the script."""
    kill_microservice()
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    # Run the script
    subprocess.run([SCRIPT_PATH], check=True)
    time.sleep(1) # Give it a moment to start and log

    last_log = get_last_log_line()
    assert re.search(r"Action:\s*STARTED$", last_log), f"Log did not indicate STARTED. Last line: {last_log}"

    assert os.path.exists(PID_FILE), "PID file was not created."
    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())
    assert is_process_running(pid), "Microservice process is not running after STARTED action."

def test_script_behavior_running():
    """Test the RUNNING state of the script."""
    # Ensure it's running from previous test or start it
    if not os.path.exists(PID_FILE):
        subprocess.run([SCRIPT_PATH], check=True)
        time.sleep(1)

    subprocess.run([SCRIPT_PATH], check=True)
    time.sleep(1)

    last_log = get_last_log_line()
    assert re.search(r"Action:\s*RUNNING$", last_log), f"Log did not indicate RUNNING. Last line: {last_log}"

def test_script_behavior_restarted():
    """Test the RESTARTED state of the script."""
    # Ensure it's running first
    if not os.path.exists(PID_FILE):
        subprocess.run([SCRIPT_PATH], check=True)
        time.sleep(1)

    with open(PID_FILE, "r") as f:
        old_pid = int(f.read().strip())

    # Kill the process but leave the PID file
    try:
        os.kill(old_pid, 9)
    except OSError:
        pass
    time.sleep(1)

    assert not is_process_running(old_pid), "Failed to kill the old process for testing."
    assert os.path.exists(PID_FILE), "PID file should still exist for this test."

    # Run the script
    subprocess.run([SCRIPT_PATH], check=True)
    time.sleep(1)

    last_log = get_last_log_line()
    assert re.search(r"Action:\s*RESTARTED$", last_log), f"Log did not indicate RESTARTED. Last line: {last_log}"

    assert os.path.exists(PID_FILE), "PID file was not created after restart."
    with open(PID_FILE, "r") as f:
        new_pid = int(f.read().strip())
    assert is_process_running(new_pid), "Microservice process is not running after RESTARTED action."
    assert old_pid != new_pid, "Process ID did not change after restart."