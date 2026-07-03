# test_final_state.py

import os
import socket
import subprocess
import time
import pytest

def test_port_forwarder():
    """
    Tests if port_forwarder.py successfully forwards traffic from 9090 to 8080
    and logs FORWARD_SUCCESS to /home/user/logs/traffic.log.
    """
    forwarder_script = "/home/user/port_forwarder.py"
    log_file = "/home/user/logs/traffic.log"

    assert os.path.exists(forwarder_script), f"Missing script: {forwarder_script}"

    # Start dummy backend on 8080
    backend_code = """
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8080))
s.listen(1)
c, a = s.accept()
c.send(b'HELLO')
c.close()
s.close()
"""
    backend_proc = subprocess.Popen(["python3", "-c", backend_code])
    time.sleep(0.5) # Wait for backend to start

    # Start port forwarder
    forwarder_proc = subprocess.Popen(["python3", forwarder_script])
    time.sleep(1.0) # Wait for forwarder to start

    try:
        # Test connectivity
        s = socket.socket()
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 9090))
        s.sendall(b'TEST\n')
        data = s.recv(1024)
        assert b'HELLO' in data, "Did not receive expected response from backend via port forwarder."
        s.close()
    finally:
        forwarder_proc.terminate()
        backend_proc.terminate()
        forwarder_proc.wait()
        backend_proc.wait()

    # Check log
    assert os.path.exists(log_file), f"Log file missing: {log_file}"
    with open(log_file, "r") as f:
        log_content = f.read()
    assert "FORWARD_SUCCESS" in log_content, f"Expected 'FORWARD_SUCCESS' in {log_file}"

def test_log_manager():
    """
    Tests if log_manager.py rotates the log file when > 1024 bytes.
    """
    log_manager_script = "/home/user/log_manager.py"
    log_file = "/home/user/logs/traffic.log"
    rotated_log = "/home/user/logs/traffic.log.1"

    assert os.path.exists(log_manager_script), f"Missing script: {log_manager_script}"

    # Setup test condition: > 1024 bytes
    with open(log_file, "wb") as f:
        f.write(os.urandom(2000))

    subprocess.run(["python3", log_manager_script], check=True)

    assert os.path.exists(rotated_log), f"Rotated log missing: {rotated_log}"
    assert os.path.getsize(rotated_log) == 2000, f"Rotated log size incorrect: expected 2000, got {os.path.getsize(rotated_log)}"

    assert os.path.exists(log_file), f"New log file missing: {log_file}"
    assert os.path.getsize(log_file) == 0, f"New log file not empty: expected 0, got {os.path.getsize(log_file)}"

def test_quota_check():
    """
    Tests if quota_check.py accurately calculates the total size of files in /home/user/logs/.
    """
    quota_check_script = "/home/user/quota_check.py"
    logs_dir = "/home/user/logs"
    report_file = "/home/user/quota_report.txt"

    assert os.path.exists(quota_check_script), f"Missing script: {quota_check_script}"

    # Clear logs dir and setup specific files
    for f in os.listdir(logs_dir):
        os.remove(os.path.join(logs_dir, f))

    with open(os.path.join(logs_dir, "traffic.log.1"), "wb") as f:
        f.write(os.urandom(2000))
    with open(os.path.join(logs_dir, "traffic.log"), "wb") as f:
        pass # 0 bytes
    with open(os.path.join(logs_dir, "extra.log"), "wb") as f:
        f.write(b"TEST\n") # 5 bytes

    subprocess.run(["python3", quota_check_script], check=True)

    assert os.path.exists(report_file), f"Report file missing: {report_file}"
    with open(report_file, "r") as f:
        report_content = f.read().strip()

    assert report_content == "TOTAL_BYTES: 2005", f"Incorrect report content: expected 'TOTAL_BYTES: 2005', got '{report_content}'"