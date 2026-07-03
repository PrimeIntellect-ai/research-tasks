# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_monitor_pid_file():
    pid_file = "/home/user/monitor.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist."
    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID in {pid_file} is not a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_network_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('127.0.0.1', 8443))
        s.sendall(b'STATUS')
        response = s.recv(1024).decode('utf-8')
        assert response == "LOCKED\n", f"Expected 'LOCKED\\n', got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail("No process listening on 127.0.0.1:8443")
    except socket.timeout:
        pytest.fail("Connection or response timed out on 127.0.0.1:8443")
    finally:
        s.close()

def test_vault_contents():
    vault_dir = "/home/user/vault"
    assert os.path.isdir(vault_dir), f"{vault_dir} is not a directory."

    file1 = os.path.join(vault_dir, "payload1.bin")
    file2 = os.path.join(vault_dir, "payload2.bin")

    assert os.path.exists(file1), f"{file1} does not exist."
    assert os.path.exists(file2), f"{file2} does not exist."

    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    assert size1 == 6000000, f"Expected {file1} to be 6000000 bytes, got {size1}"
    assert size2 == 5000000, f"Expected {file2} to be 5000000 bytes, got {size2}"
    assert size1 + size2 == 11000000, "Total size of payload files is not 11000000."

def test_vault_state_log():
    log_file = "/home/user/vault_state.log"
    assert os.path.exists(log_file), f"{log_file} does not exist."
    with open(log_file, 'r') as f:
        content = f.read().strip()

    assert content == "LOCKED: 11000000", f"Unexpected content in {log_file}: {content}"

def test_expect_script_exists():
    script_file = "/home/user/simulate_uploads.exp"
    assert os.path.exists(script_file), f"{script_file} does not exist."
    with open(script_file, 'r') as f:
        content = f.read()

    assert "spawn" in content, f"spawn command not found in {script_file}"
    assert "expect" in content, f"expect command not found in {script_file}"
    assert "send" in content, f"send command not found in {script_file}"

def test_uploader_not_running():
    try:
        output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

    running = False
    for line in output.splitlines():
        if "interactive_uploader.py" in line and "grep" not in line and "simulate_uploads.exp" not in line:
            running = True
            break

    assert not running, "interactive_uploader.py is still running, it should have been killed."