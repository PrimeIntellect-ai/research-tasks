# test_final_state.py

import os
import stat
import pytest

def test_watchdog_exists_and_executable():
    watchdog_path = "/home/user/watchdog"
    assert os.path.isfile(watchdog_path), f"Missing file: {watchdog_path}"

    st = os.stat(watchdog_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File is not executable: {watchdog_path}"

def test_outbox_permissions():
    outbox_path = "/home/user/outbox"
    assert os.path.isdir(outbox_path), f"Missing directory: {outbox_path}"

    st = os.stat(outbox_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Incorrect permissions on {outbox_path}, expected 0o700 but got {oct(perms)}"

def test_watchdog_log_contents():
    log_path = "/home/user/watchdog.log"
    assert os.path.isfile(log_path), f"Missing file: {log_path}"

    with open(log_path, 'r') as f:
        lines = f.readlines()

    alert_lines = [line for line in lines if line.strip() == "[ALERT] Child crashed"]
    assert len(alert_lines) == 3, f"Expected exactly 3 alerts in {log_path}, found {len(alert_lines)}"

def test_alerts_eml_contents():
    eml_path = "/home/user/outbox/alerts.eml"
    assert os.path.isfile(eml_path), f"Missing file: {eml_path}"

    with open(eml_path, 'r') as f:
        lines = f.readlines()

    subject_lines = [line for line in lines if line.strip() == "Subject: Edge Device Alert - Process Restarted"]
    assert len(subject_lines) == 3, f"Expected exactly 3 subjects in {eml_path}, found {len(subject_lines)}"