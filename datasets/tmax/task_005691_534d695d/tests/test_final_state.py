# test_final_state.py

import os
import re
import stat
import pytest

APP_DIR = "/home/user/app"
WRAPPER_SCRIPT = os.path.join(APP_DIR, "run_monitor.sh")
MONITOR_SCRIPT = os.path.join(APP_DIR, "mail_monitor.py")
OUTPUT_DIR = os.path.join(APP_DIR, "output")
LOG_FILE = os.path.join(OUTPUT_DIR, "report.log")

def test_wrapper_script_exists_and_executable():
    """Verify the wrapper script exists and is executable."""
    assert os.path.isfile(WRAPPER_SCRIPT), f"Wrapper script {WRAPPER_SCRIPT} is missing."
    st = os.stat(WRAPPER_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script {WRAPPER_SCRIPT} is not executable."

def test_wrapper_script_contents():
    """Verify the wrapper script exports the variable and calls the python script."""
    with open(WRAPPER_SCRIPT, 'r') as f:
        content = f.read()

    assert "SMTP_SERVER_IP" in content and "127.0.0.1" in content, \
        "Wrapper script does not seem to export SMTP_SERVER_IP='127.0.0.1'."
    assert "mail_monitor.py" in content, \
        "Wrapper script does not execute mail_monitor.py."

def test_monitor_script_contents():
    """Verify the Python script contains the required logic."""
    assert os.path.isfile(MONITOR_SCRIPT), f"Python script {MONITOR_SCRIPT} is missing."
    with open(MONITOR_SCRIPT, 'r') as f:
        content = f.read()

    assert "127.0.0.1" in content, "Python script does not default to 127.0.0.1."
    assert "/home/user/app/output/report.log" in content, "Python script does not use the absolute path for the log file."
    assert "10255" in content, "Python script does not use port 10255."
    assert "STATUS: OK" in content, "Python script does not contain 'STATUS: OK'."
    assert "STATUS: ERROR" in content, "Python script does not contain 'STATUS: ERROR'."

def test_output_directory_and_log_exist():
    """Verify the output directory and log file exist."""
    assert os.path.isdir(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} was not created."
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not generated."

def test_log_contains_status_ok():
    """Verify the log file contains STATUS: OK."""
    with open(LOG_FILE, 'r') as f:
        content = f.read()

    assert "STATUS: OK" in content, "Log file does not contain 'STATUS: OK'. Ensure the wrapper script was executed manually."