# test_final_state.py
import os
import urllib.request
import re

def test_wrapper_script_modifications():
    wrapper_path = "/home/user/run_monitor.sh"
    assert os.path.isfile(wrapper_path), f"Wrapper script {wrapper_path} is missing."

    with open(wrapper_path, "r") as f:
        content = f.read()

    # Check for MONITOR_LOG_DIR
    assert "MONITOR_LOG_DIR=/home/user/logs" in content or "MONITOR_LOG_DIR=\"/home/user/logs\"" in content or "MONITOR_LOG_DIR='/home/user/logs'" in content, \
        "Wrapper script does not properly set MONITOR_LOG_DIR to /home/user/logs."

    # Check for PATH modification
    assert "/home/user/bin" in content and "PATH" in content, \
        "Wrapper script does not append /home/user/bin to PATH."

def test_python_script_no_absolute_path():
    py_path = "/home/user/monitor_uptime.py"
    assert os.path.isfile(py_path), f"Python script {py_path} is missing."

    with open(py_path, "r") as f:
        content = f.read()

    assert "/home/user/bin/get_disk_usage" not in content, \
        "Python script should not use the absolute path for get_disk_usage."

def test_log_file_created_and_accurate():
    log_path = "/home/user/logs/uptime.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Log file is empty."

    # Check the last line or any line for the correct output
    expected_log = "STATUS: UP, DISK: 42%"
    found = any(expected_log in line for line in lines)
    assert found, f"Expected log line containing '{expected_log}' not found in {log_path}."

def test_webserver_running():
    # The server might still be running. If not, the log file check is the primary verification,
    # but we can check if we can connect to 127.0.0.1:8000.
    # The prompt says "Start a dummy HTTP server ... in the background".
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8000", timeout=2)
        assert response.getcode() == 200, "Webserver is running but did not return HTTP 200."
    except Exception as e:
        # If the server stopped but the log is correct, we might still fail this if the prompt strictly requires it to be running.
        # "Start a dummy HTTP server ... in the background" implies it should still be running.
        assert False, f"Could not connect to the dummy webserver on 127.0.0.1:8000: {e}"