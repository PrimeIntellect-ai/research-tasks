# test_final_state.py

import os
import stat
import subprocess
import socket
import threading
import time
import pytest

def test_bashrc_updated():
    """Check that .bashrc exports HUB_PORT=8888."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "export HUB_PORT=8888" in content, "HUB_PORT=8888 is not exported in .bashrc."

def test_heartbeat_files():
    """Check that heartbeat.c and heartbeat binary exist, and binary is executable."""
    c_path = "/home/user/heartbeat.c"
    bin_path = "/home/user/heartbeat"
    assert os.path.isfile(c_path), f"{c_path} does not exist."
    assert os.path.isfile(bin_path), f"{bin_path} does not exist."
    st = os.stat(bin_path)
    assert st.st_mode & stat.S_IXUSR, f"{bin_path} is not executable."

def test_heartbeat_execution_fail():
    """Check heartbeat behavior when connection fails."""
    env = os.environ.copy()
    env["HUB_PORT"] = "8888"

    # Ensure no server is running on 8888
    result = subprocess.run(["/home/user/heartbeat"], env=env, capture_output=True, text=True)

    assert result.returncode == 1, f"Expected exit code 1, got {result.returncode}"
    assert result.stdout == "CONNECTION_FAILED\n", f"Expected 'CONNECTION_FAILED\\n', got {repr(result.stdout)}"

def test_heartbeat_execution_success():
    """Check heartbeat behavior when connection succeeds."""
    env = os.environ.copy()
    env["HUB_PORT"] = "8888"

    received_data = []

    def server_thread():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 8888))
        s.listen(1)
        s.settimeout(5)
        try:
            conn, addr = s.accept()
            data = b""
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk
            received_data.append(data)
            conn.close()
        except socket.timeout:
            pass
        finally:
            s.close()

    t = threading.Thread(target=server_thread)
    t.start()

    # Give server a moment to start
    time.sleep(0.5)

    result = subprocess.run(["/home/user/heartbeat"], env=env, capture_output=True, text=True)
    t.join()

    assert result.returncode == 2, f"Expected exit code 2, got {result.returncode}"
    expected_stdout = "HEARTBEAT_SENT\n" * 5
    assert result.stdout == expected_stdout, f"Expected 5x HEARTBEAT_SENT, got {repr(result.stdout)}"

    assert len(received_data) == 1, "Server did not receive data."
    assert received_data[0] == b"PING\n" * 5, f"Expected 5x PING\\n, got {repr(received_data[0])}"

def test_supervisor_files():
    """Check that supervisor.sh exists and is executable."""
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"{script_path} is not executable."

def test_health_check_files():
    """Check that health_check.sh exists and is executable."""
    script_path = "/home/user/health_check.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"{script_path} is not executable."

def test_health_check_behavior():
    """Check the logic of health_check.sh with mock logs."""
    os.makedirs("/home/user/logs", exist_ok=True)
    log_file = "/home/user/logs/edge.log"
    old_log_file = "/home/user/logs/edge.log.old"

    # Clear logs
    if os.path.exists(log_file): os.remove(log_file)
    if os.path.exists(old_log_file): os.remove(old_log_file)

    # Test FAIL state
    result = subprocess.run(["/home/user/health_check.sh"], capture_output=True, text=True)
    assert result.returncode == 1, "Expected exit code 1 when logs are empty/nonexistent."
    assert "STATUS: FAIL" in result.stdout, "Expected 'STATUS: FAIL' in stdout."

    # Test OK state
    with open(log_file, "w") as f:
        f.write("CONNECTION_FAILED\nHEARTBEAT_SENT\n")

    result = subprocess.run(["/home/user/health_check.sh"], capture_output=True, text=True)
    assert result.returncode == 0, "Expected exit code 0 when HEARTBEAT_SENT is in logs."
    assert "STATUS: OK" in result.stdout, "Expected 'STATUS: OK' in stdout."

def test_supervisor_behavior():
    """Check if supervisor.sh runs heartbeat, logs output, and rotates log."""
    # Ensure clean state
    os.makedirs("/home/user/logs", exist_ok=True)
    log_file = "/home/user/logs/edge.log"
    old_log_file = "/home/user/logs/edge.log.old"
    if os.path.exists(log_file): os.remove(log_file)
    if os.path.exists(old_log_file): os.remove(old_log_file)

    # Run supervisor in background
    proc = subprocess.Popen(["/home/user/supervisor.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait enough time for 6 failures (6 * 1s sleep = ~6 seconds) + some buffer
        time.sleep(8)
    finally:
        proc.terminate()
        proc.wait(timeout=2)

    assert os.path.isdir("/home/user/logs"), "Supervisor did not create /home/user/logs directory."
    assert os.path.isfile(old_log_file), "Supervisor did not rotate the log to edge.log.old after exceeding 100 bytes."