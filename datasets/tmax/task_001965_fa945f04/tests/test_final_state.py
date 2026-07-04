# test_final_state.py

import os
import socket
import time
import glob

HOST = '127.0.0.1'
PORT = 8844
TOKEN = 'SEC-99-BKUP-X7'

def send_request(payload: bytes) -> bytes:
    try:
        with socket.create_connection((HOST, PORT), timeout=2) as s:
            s.sendall(payload)
            response = s.recv(1024)
            return response
    except Exception as e:
        return b""

def test_daemon_running():
    """Verify that the daemon is listening on the correct port."""
    try:
        with socket.create_connection((HOST, PORT), timeout=2):
            pass
    except Exception as e:
        assert False, f"Could not connect to daemon on {HOST}:{PORT}. Is it running? Error: {e}"

def test_valid_interaction():
    """Verify that a valid token and payload results in OK and saves the backup."""
    # Count files before
    backup_dir = "/home/user/backups"
    os.makedirs(backup_dir, exist_ok=True)
    files_before = set(os.listdir(backup_dir))

    payload_data = "system_config_v1_backup_test123"
    req = f"TOKEN:{TOKEN}|PAYLOAD:{payload_data}\n".encode('utf-8')

    resp = send_request(req)
    assert resp == b"OK\n", f"Expected 'OK\\n' for valid request, got: {resp!r}"

    time.sleep(0.5)
    files_after = set(os.listdir(backup_dir))
    new_files = files_after - files_before

    assert len(new_files) > 0, "No new backup file was created in /home/user/backups/"

    found_payload = False
    for nf in new_files:
        with open(os.path.join(backup_dir, nf), 'r') as f:
            content = f.read()
            if payload_data in content:
                found_payload = True
                break

    assert found_payload, f"The payload '{payload_data}' was not found in any of the newly created backup files."

def test_invalid_token_interaction():
    """Verify that an invalid token results in ERR: Unauthorized."""
    req = b"TOKEN:WRONG-TOKEN|PAYLOAD:rogue_data\n"
    resp = send_request(req)
    assert resp == b"ERR: Unauthorized\n", f"Expected 'ERR: Unauthorized\\n' for invalid token, got: {resp!r}"

def test_malformed_interaction():
    """Verify that a malformed request results in ERR: Unauthorized."""
    req = b"BADFORMAT\n"
    resp = send_request(req)
    assert resp == b"ERR: Unauthorized\n", f"Expected 'ERR: Unauthorized\\n' for malformed request, got: {resp!r}"

def test_files_exist():
    """Verify that the required source and script files exist."""
    assert os.path.exists("/home/user/backup_daemon.c"), "/home/user/backup_daemon.c is missing."
    assert os.path.exists("/home/user/manage_backup.sh"), "/home/user/manage_backup.sh is missing."
    assert os.path.exists("/home/user/backup_daemon.pid"), "/home/user/backup_daemon.pid is missing."