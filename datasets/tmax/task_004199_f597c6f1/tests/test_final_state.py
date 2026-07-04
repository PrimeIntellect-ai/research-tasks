# test_final_state.py

import os
import socket
import subprocess
import time
import re
import glob
import pytest

PIN = "4826"
HAPROXY_HOST = "127.0.0.1"
HAPROXY_PORT = 8080

def send_tcp_request(host, port, message):
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        return str(e)

def test_telemetry_daemon_auth_success():
    """Test successful authentication through HAProxy."""
    response = send_tcp_request(HAPROXY_HOST, HAPROXY_PORT, f"AUTH {PIN}\n")
    assert response == "TELEMETRY_ACK\n", f"Expected 'TELEMETRY_ACK\\n', got '{response}'"

def test_telemetry_daemon_auth_failure():
    """Test failed authentication silently closes connection."""
    response = send_tcp_request(HAPROXY_HOST, HAPROXY_PORT, "AUTH 1234\n")
    # It might return empty string (closed connection) or an error, but not TELEMETRY_ACK
    assert response != "TELEMETRY_ACK\n", "Expected connection to be closed without ACK, but received TELEMETRY_ACK"
    assert response == "", f"Expected empty response (closed connection), got '{response}'"

def test_log_file_exists_and_format():
    """Check that the log file exists and contains the correct format."""
    log_file = "/home/user/logs/telemetry.log"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    assert "Connection received" in content, "Log file does not contain 'Connection received'."

def test_rotate_and_backup_script():
    """Test the rotate and backup script functionality."""
    script_path = "/home/user/rotate_and_backup.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the backup script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Backup script failed with output: {result.stderr}"

    # Give it a moment to restart/signal
    time.sleep(1)

    # Check that a backup file was created
    backup_dir = "/home/user/backups"
    assert os.path.exists(backup_dir), f"Backup directory {backup_dir} does not exist."

    backup_files = glob.glob(os.path.join(backup_dir, "telemetry_*.log"))
    assert len(backup_files) > 0, "No backup file found matching telemetry_*.log"

    # Verify the service still works
    response = send_tcp_request(HAPROXY_HOST, HAPROXY_PORT, f"AUTH {PIN}\n")
    assert response == "TELEMETRY_ACK\n", f"Service did not respond correctly after backup script execution. Got: '{response}'"

    # Verify a new log file was created
    log_file = "/home/user/logs/telemetry.log"
    assert os.path.exists(log_file), "New log file was not created after backup."

    with open(log_file, "r") as f:
        content = f.read()

    assert "Connection received" in content, "New log file does not contain 'Connection received' after post-backup request."