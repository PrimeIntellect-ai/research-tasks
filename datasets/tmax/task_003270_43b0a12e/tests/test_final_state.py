# test_final_state.py
import os
import socket
import struct
import time
import pytest

HOST = '127.0.0.1'
PORT = 8088
TOKEN = b"TKN-9942-ALPHA"
WRONG_TOKEN = b"TKN-0000-WRONG"
MAGIC = b"\x41\x55\x54\x5A"
WRONG_MAGIC = b"\x00\x00\x00\x00"

def test_source_code_exists():
    assert os.path.isfile("/home/user/mock_authz.c"), "The C source code /home/user/mock_authz.c is missing."

def test_build_script_exists_and_executable():
    script_path = "/home/user/build_and_deploy.sh"
    assert os.path.isfile(script_path), f"The build script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The build script {script_path} is not executable."

def test_pid_file_exists():
    pid_file = "/home/user/mock_authz.pid"
    assert os.path.isfile(pid_file), f"The PID file {pid_file} is missing."
    with open(pid_file, 'r') as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    # Check if process is running
    assert os.path.exists(f"/proc/{pid}"), f"Process with PID {pid} is not running."

def send_request(magic, payload):
    length = struct.pack(">H", len(payload))
    packet = magic + length + payload

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
            s.sendall(packet)
            response = s.recv(4)
            return response
        except Exception as e:
            pytest.fail(f"Connection or communication failed: {e}")

def test_valid_request():
    response = send_request(MAGIC, TOKEN)
    assert response == b"\x4F\x4B\x41\x59", f"Expected OKAY (0x4F4B4159), got {response}"

def test_invalid_request_wrong_token():
    response = send_request(MAGIC, WRONG_TOKEN)
    assert response == b"\x46\x41\x49\x4C", f"Expected FAIL (0x4641494C), got {response}"

def test_invalid_request_wrong_magic():
    response = send_request(WRONG_MAGIC, TOKEN)
    assert response == b"\x46\x41\x49\x4C", f"Expected FAIL (0x4641494C), got {response}"