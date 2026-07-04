# test_final_state.py

import os
import re
import socket
import subprocess

def test_monitor_script_exists():
    assert os.path.isfile("/home/user/monitor.py"), "The script /home/user/monitor.py does not exist."

def test_monitor_is_running():
    # Check if monitor.py is running in the process list
    try:
        output = subprocess.check_output(["pgrep", "-f", "monitor.py"]).decode("utf-8")
        assert len(output.strip()) > 0, "monitor.py is not running in the background."
    except subprocess.CalledProcessError:
        assert False, "monitor.py is not running in the background."

def test_monitoring_log_format():
    log_path = "/home/user/monitoring.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist. Did the monitor detect a crash?"

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) > 0, f"The log file {log_path} is empty."

    # Check if at least one line matches the expected format
    pattern = re.compile(r"^ALERT: Service failure detected at \d+$")
    match_found = any(pattern.match(line) for line in content)

    assert match_found, f"No line in {log_path} matches the required format 'ALERT: Service failure detected at <UNIX_TIMESTAMP>'."

def test_service_is_running_and_listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        result = s.connect_ex(('127.0.0.1', 8888))
        assert result == 0, "The service is not listening on 127.0.0.1:8888. The monitor may have failed to restart it."
    finally:
        s.close()