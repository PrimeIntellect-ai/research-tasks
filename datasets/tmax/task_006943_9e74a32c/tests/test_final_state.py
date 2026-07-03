# test_final_state.py

import os
import stat
import subprocess
import time
import re
import pytest

ENFORCER_SCRIPT = "/home/user/enforcer.sh"
SYSTEMD_DIR = "/home/user/.config/systemd/user"
SERVICE_FILE = os.path.join(SYSTEMD_DIR, "enforcer.service")
TIMER_FILE = os.path.join(SYSTEMD_DIR, "enforcer.timer")
APP_DATA_DIR = "/home/user/app_data"
MAIL_SPOOL_DIR = "/home/user/mail_spool"
LOG_FILE = "/home/user/enforcement.log"

def test_enforcer_script_exists_and_executable():
    assert os.path.isfile(ENFORCER_SCRIPT), f"{ENFORCER_SCRIPT} does not exist."
    st = os.stat(ENFORCER_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{ENFORCER_SCRIPT} is not executable."

def test_systemd_files_exist():
    assert os.path.isfile(SERVICE_FILE), f"{SERVICE_FILE} does not exist."
    assert os.path.isfile(TIMER_FILE), f"{TIMER_FILE} does not exist."

def test_systemd_timer_active_and_enabled():
    env = os.environ.copy()
    env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"

    res_active = subprocess.run(["systemctl", "--user", "is-active", "enforcer.timer"], capture_output=True, text=True, env=env)
    assert res_active.returncode == 0, "enforcer.timer is not active."

    res_enabled = subprocess.run(["systemctl", "--user", "is-enabled", "enforcer.timer"], capture_output=True, text=True, env=env)
    assert res_enabled.returncode == 0, "enforcer.timer is not enabled."

def test_functional_enforcement():
    # Setup test condition
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    os.makedirs(MAIL_SPOOL_DIR, exist_ok=True)

    tmp_file = os.path.join(APP_DATA_DIR, "dummy.tmp")
    with open(tmp_file, "wb") as f:
        f.write(b"0" * (6 * 1024 * 1024)) # 6 MB

    # Start a process that accesses the directory
    proc = subprocess.Popen(["sleep", "300"], cwd=APP_DATA_DIR)
    pid = proc.pid

    # Allow process to start
    time.sleep(1)

    # Run the enforcer script
    run_res = subprocess.run([ENFORCER_SCRIPT], capture_output=True, text=True)

    # Give it a moment to kill and log
    time.sleep(1)

    # Check if process is killed
    proc_poll = proc.poll()
    if proc_poll is None:
        proc.kill()
        pytest.fail(f"Process {pid} was not killed by the enforcer script.")

    # Check if .tmp file is deleted
    assert not os.path.exists(tmp_file), f".tmp files in {APP_DATA_DIR} were not deleted."

    # Check log file
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not created."
    with open(LOG_FILE, "r") as f:
        logs = f.read()

    expected_log_pattern = rf"\[\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\] ACTION=KILL PID={pid} DIR=/home/user/app_data EXCEEDED_QUOTA"
    assert re.search(expected_log_pattern, logs), f"Expected log entry for PID {pid} not found in {LOG_FILE}."

    # Check mail spool
    mail_file = os.path.join(MAIL_SPOOL_DIR, f"alert_{pid}.eml")
    assert os.path.isfile(mail_file), f"Mail spool file {mail_file} was not created."

    with open(mail_file, "r") as f:
        mail_content = f.read()

    expected_mail = f"""To: admin@local.domain
From: monitor@local.domain
Subject: Quota Alert - Process Terminated

Process {pid} was terminated for exceeding the 5000KB limit in /home/user/app_data.
"""
    assert mail_content.strip() == expected_mail.strip(), "Mail spool file contents do not match the required format."