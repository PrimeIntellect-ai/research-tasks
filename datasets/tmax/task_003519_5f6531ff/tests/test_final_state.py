# test_final_state.py

import os
import socket
import pytest

HOST = '127.0.0.1'
PORT = 8888
TOKEN = "TKN-88X9-A"

def test_files_exist():
    c_file = "/home/user/new_diagd.c"
    bin_file = "/home/user/new_diagd"

    assert os.path.isfile(c_file), f"Expected C source file {c_file} to exist."
    assert os.path.isfile(bin_file), f"Expected compiled binary {bin_file} to exist."
    assert os.access(bin_file, os.X_OK), f"Expected {bin_file} to be executable."

def send_and_receive(sock, message, buffer_size=1024):
    sock.sendall(message.encode('utf-8'))
    response = sock.recv(buffer_size).decode('utf-8')
    return response

def test_valid_auth():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the daemon running?")

        response = send_and_receive(s, f"AUTH {TOKEN}\n")
        assert response == "AUTH_OK\n", f"Expected 'AUTH_OK\\n', got {repr(response)}"

def test_invalid_auth():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the daemon running?")

        response = send_and_receive(s, "AUTH INVALID\n")
        assert response == "AUTH_FAIL\n", f"Expected 'AUTH_FAIL\\n', got {repr(response)}"

        # Check if connection is closed
        try:
            extra = s.recv(1024)
            assert not extra, "Expected connection to be closed after invalid auth."
        except (socket.timeout, ConnectionResetError):
            pass # Expected behavior

def test_valid_cmd():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the daemon running?")

        auth_resp = send_and_receive(s, f"AUTH {TOKEN}\n")
        assert auth_resp == "AUTH_OK\n", f"Auth failed, got {repr(auth_resp)}"

        cmd_resp = send_and_receive(s, "CMD 0005 hello\n")
        assert cmd_resp == "CMD_RECV 5\n", f"Expected 'CMD_RECV 5\\n', got {repr(cmd_resp)}"

def test_large_cmd():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the daemon running?")

        auth_resp = send_and_receive(s, f"AUTH {TOKEN}\n")
        assert auth_resp == "AUTH_OK\n", f"Auth failed, got {repr(auth_resp)}"

        cmd_resp = send_and_receive(s, "CMD FFFF exploitpayload\n")
        assert cmd_resp == "ERR_TOO_LARGE\n", f"Expected 'ERR_TOO_LARGE\\n', got {repr(cmd_resp)}"