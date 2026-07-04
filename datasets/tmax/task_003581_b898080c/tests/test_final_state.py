# test_final_state.py

import os
import socket
import re
import pytest

def test_daemon_listening_and_responding():
    """Verify that the daemon is listening on 127.0.0.1:8888 and responds correctly."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(("127.0.0.1", 8888))
        data = s.recv(1024).decode('utf-8')
        assert "Welcome to AccountMgr. Enter command (ADD/DEL/QUIT):" in data, "Daemon did not send the expected welcome message."

        s.sendall(b"ADD\n")
        data2 = s.recv(1024).decode('utf-8')
        assert "Username:" in data2, "Daemon did not prompt for Username."

        s.sendall(b"admin_xyz\n")
        data3 = s.recv(1024).decode('utf-8')
        assert "Success. Account created." in data3, "Daemon did not send success message."
    except ConnectionRefusedError:
        pytest.fail("Connection refused: The daemon is not listening on 127.0.0.1:8888.")
    except socket.timeout:
        pytest.fail("Connection timed out: The daemon is not responding correctly.")
    finally:
        s.close()

def test_c_code_fixed():
    """Verify that the C code was fixed to use htons."""
    file_path = "/home/user/account_daemon.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "htons" in content and "8888" in content, "The C code does not appear to be fixed with htons(8888)."

def test_expect_script_exists_and_valid():
    """Verify the Expect script exists and uses nc."""
    file_path = "/home/user/add_user.exp"
    assert os.path.isfile(file_path), f"Expect script {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "spawn" in content, "The file does not appear to be a valid Expect script (missing 'spawn')."
    assert "nc" in content and "127.0.0.1" in content and "8888" in content, "The Expect script does not appear to spawn 'nc 127.0.0.1 8888'."
    assert "expect" in content and "send" in content, "The Expect script is missing 'expect' or 'send' commands."

def test_result_log_content():
    """Verify the result log contains the success message."""
    file_path = "/home/user/result.log"
    assert os.path.isfile(file_path), f"Log file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "Success. Account created." in content, f"The log file {file_path} does not contain the expected success message."