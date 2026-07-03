# test_final_state.py
import os
import socket
import hashlib
import time
import subprocess
import pytest

def get_server_pid(port=9000):
    """Find the PID of the process listening on the specified port."""
    try:
        # Try using ss first
        output = subprocess.check_output(['ss', '-lptn'], text=True)
        for line in output.splitlines():
            if f":{port}" in line and "upload_server" in line:
                parts = line.split("pid=")
                if len(parts) > 1:
                    return int(parts[1].split(',')[0])
    except Exception:
        pass

    try:
        # Fallback to pgrep
        output = subprocess.check_output(['pgrep', '-x', 'upload_server'], text=True)
        pids = [int(p) for p in output.split()]
        if pids:
            return pids[0]
    except Exception:
        pass
    return None

def send_file(filename, content, force_hash=None):
    """Send a file payload to the server using the custom protocol."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 9000))
        actual_hash = hashlib.sha256(content).hexdigest()
        hash_to_send = force_hash if force_hash else actual_hash

        padded_filename = filename.ljust(256, '\x00')
        payload = hash_to_send.encode('ascii') + padded_filename.encode('ascii') + content
        s.sendall(payload)
    except ConnectionRefusedError:
        pytest.fail("Connection refused. The server is not running or listening on port 9000.")
    finally:
        s.close()

def test_upload_server_executable():
    binary_path = "/home/user/upload_server"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_server_running_and_seccomp_enabled():
    pid = get_server_pid()
    assert pid is not None, "upload_server is not running or not listening on port 9000."

    status_file = f"/proc/{pid}/status"
    assert os.path.exists(status_file), f"Process status file {status_file} not found."

    with open(status_file, 'r') as f:
        status_content = f.read()

    seccomp_enabled = False
    for line in status_content.splitlines():
        if line.startswith("Seccomp:"):
            val = line.split(':')[1].strip()
            # 2 means SECCOMP_MODE_FILTER
            if val == "2":
                seccomp_enabled = True
            break

    assert seccomp_enabled, f"Seccomp filter mode is not enabled for PID {pid}. Sandboxing is missing."

def test_vulnerabilities_and_logging():
    log_file = "/home/user/server.log"

    # Clear log file before test to ensure we only read our test results
    if os.path.exists(log_file):
        open(log_file, 'w').close()

    # 1. Path Traversal
    # SHA256("test") = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
    send_file("../../../etc/passwd", b"test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")
    time.sleep(0.5)

    # 2. Hash Mismatch
    send_file("valid_file.txt", b"test", "0000000000000000000000000000000000000000000000000000000000000000")
    time.sleep(0.5)

    # 3. Valid File
    send_file("good_file.bin", b"Secret data inside!")
    time.sleep(0.5)

    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, 'r') as f:
        log_content = f.read()

    expected_logs = [
        "REJECTED: Path traversal attempt: ../../../etc/passwd",
        "REJECTED: Hash mismatch for valid_file.txt",
        "ACCEPTED: good_file.bin"
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log entry '{expected}' not found in {log_file}."

    # Verify good file was saved correctly
    saved_file = "/home/user/uploads/good_file.bin"
    assert os.path.exists(saved_file), f"Valid file was not saved to {saved_file}."
    with open(saved_file, 'rb') as f:
        assert f.read() == b"Secret data inside!", f"Content of {saved_file} does not match the sent payload."

    # Verify bad files were not saved
    assert not os.path.exists("/home/user/uploads/valid_file.txt"), "File with mismatched hash was saved."
    assert not os.path.exists("/home/user/uploads/passwd"), "Path traversal file was partially saved."