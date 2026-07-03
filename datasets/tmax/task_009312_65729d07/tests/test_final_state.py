# test_final_state.py

import os
import stat
import subprocess
import shutil
import pytest

HOME_DIR = "/home/user"
INBOX_DIR = os.path.join(HOME_DIR, "provision_inbox")
ARCHIVE_DIR = os.path.join(HOME_DIR, "provision_archive")
WATCHER_SCRIPT = os.path.join(HOME_DIR, "watcher.sh")
LOG_FILE = os.path.join(HOME_DIR, "provision.log")
SERVICE_FILE = os.path.join(HOME_DIR, ".config/systemd/user/provision-watcher.service")
TIMER_FILE = os.path.join(HOME_DIR, ".config/systemd/user/provision-watcher.timer")
HEALTH_SCRIPT = os.path.join(HOME_DIR, "health.sh")

def test_directories_exist():
    assert os.path.isdir(INBOX_DIR), f"Directory {INBOX_DIR} does not exist."
    assert os.path.isdir(ARCHIVE_DIR), f"Directory {ARCHIVE_DIR} does not exist."

def test_watcher_script_exists_and_executable():
    assert os.path.isfile(WATCHER_SCRIPT), f"Script {WATCHER_SCRIPT} does not exist."
    st = os.stat(WATCHER_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {WATCHER_SCRIPT} is not executable."

def test_watcher_script_behavior():
    # Setup test files
    test1 = os.path.join(INBOX_DIR, "test1.txt")
    test2 = os.path.join(INBOX_DIR, "test2.txt")
    ignore = os.path.join(INBOX_DIR, "ignore.json")

    with open(test1, "w") as f: f.write("1")
    with open(test2, "w") as f: f.write("2")
    with open(ignore, "w") as f: f.write("3")

    # Run the watcher script
    result = subprocess.run([WATCHER_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{WATCHER_SCRIPT} failed to execute."

    # Check if files were moved
    assert os.path.isfile(os.path.join(ARCHIVE_DIR, "test1.txt")), "test1.txt was not moved to the archive."
    assert os.path.isfile(os.path.join(ARCHIVE_DIR, "test2.txt")), "test2.txt was not moved to the archive."
    assert os.path.isfile(ignore), "ignore.json should not have been moved."
    assert not os.path.isfile(test1), "test1.txt was not removed from inbox."
    assert not os.path.isfile(test2), "test2.txt was not removed from inbox."

    # Check log file
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not created."
    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    assert "PROVISIONED: test1.txt" in log_content, "Log file missing entry for test1.txt."
    assert "PROVISIONED: test2.txt" in log_content, "Log file missing entry for test2.txt."

def test_systemd_service():
    assert os.path.isfile(SERVICE_FILE), f"Systemd service file {SERVICE_FILE} does not exist."
    with open(SERVICE_FILE, "r") as f:
        content = f.read()
    assert "ExecStart=/home/user/watcher.sh" in content, f"Service file missing correct ExecStart."
    assert "Description=Provision Watcher" in content, f"Service file missing correct Description."

def test_systemd_timer():
    assert os.path.isfile(TIMER_FILE), f"Systemd timer file {TIMER_FILE} does not exist."
    with open(TIMER_FILE, "r") as f:
        content = f.read()
    assert "OnCalendar=*:0/2" in content, f"Timer file missing correct OnCalendar value."

def test_health_script_exists_and_executable():
    assert os.path.isfile(HEALTH_SCRIPT), f"Script {HEALTH_SCRIPT} does not exist."
    st = os.stat(HEALTH_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {HEALTH_SCRIPT} is not executable."

def test_health_script_behavior():
    # Ensure log file exists for STATUS: OK test
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f: f.write("test")

    result = subprocess.run([HEALTH_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{HEALTH_SCRIPT} failed to execute."
    assert result.stdout.strip() == "STATUS: OK", f"Health script did not output 'STATUS: OK' when log exists."

    # Remove log file for STATUS: PENDING test
    os.remove(LOG_FILE)
    result = subprocess.run([HEALTH_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{HEALTH_SCRIPT} failed to execute."
    assert result.stdout.strip() == "STATUS: PENDING", f"Health script did not output 'STATUS: PENDING' when log is missing."