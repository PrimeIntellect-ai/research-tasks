# test_final_state.py

import os
import socket
import pytest

BASE_DIR = "/home/user/deploy_system"
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
PAYLOAD_FILE = os.path.join(PUBLIC_DIR, "payload.json")
MANAGER_SCRIPT = os.path.join(BASE_DIR, "manager.py")
CERT_FILE = os.path.join(BASE_DIR, "cert.pem")
KEY_FILE = os.path.join(BASE_DIR, "key.pem")
TEST_RESULT_FILE = os.path.join(BASE_DIR, "test_result.txt")
APP_PID_FILE = os.path.join(BASE_DIR, "app.pid")
APP_LOG_FILE = os.path.join(BASE_DIR, "app.log")

def test_payload_file():
    """Verify the payload.json file exists and has the correct content."""
    assert os.path.exists(PAYLOAD_FILE), f"File {PAYLOAD_FILE} does not exist."
    with open(PAYLOAD_FILE, "r") as f:
        content = f.read().strip()
    assert content == '{"status": "securely deployed"}', f"Incorrect content in {PAYLOAD_FILE}."

def test_manager_script_exists():
    """Verify the manager.py script exists."""
    assert os.path.exists(MANAGER_SCRIPT), f"File {MANAGER_SCRIPT} does not exist."
    assert os.path.isfile(MANAGER_SCRIPT), f"{MANAGER_SCRIPT} is not a file."

def test_certificates_exist():
    """Verify the TLS certificate and key exist."""
    assert os.path.exists(CERT_FILE), f"Certificate file {CERT_FILE} does not exist."
    assert os.path.exists(KEY_FILE), f"Key file {KEY_FILE} does not exist."

def test_test_result_file():
    """Verify the curl test result exists and has the correct output."""
    assert os.path.exists(TEST_RESULT_FILE), f"File {TEST_RESULT_FILE} does not exist."
    with open(TEST_RESULT_FILE, "r") as f:
        content = f.read().strip()
    assert '{"status": "securely deployed"}' in content, f"Incorrect content in {TEST_RESULT_FILE}."

def test_pid_file_cleaned_up():
    """Verify the PID file was deleted after stopping the server."""
    assert not os.path.exists(APP_PID_FILE), f"PID file {APP_PID_FILE} still exists, indicating the server was not stopped cleanly."

def test_log_file_exists():
    """Verify the application log file exists."""
    assert os.path.exists(APP_LOG_FILE), f"Log file {APP_LOG_FILE} does not exist."

def test_port_9443_is_free():
    """Verify that port 9443 is no longer in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', 9443))
        assert result != 0, "Port 9443 is still in use. The server process was not properly terminated."