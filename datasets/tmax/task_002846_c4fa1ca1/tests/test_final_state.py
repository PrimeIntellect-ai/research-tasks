# test_final_state.py

import os
import stat
import socket
import subprocess
import time
import pytest

DAEMON_C = "/home/user/account_daemon.c"
DAEMON_BIN = "/home/user/account_daemon"
SERVICE_SH = "/home/user/service.sh"
PID_FILE = "/home/user/account_daemon.pid"
SOCK_FILE = "/home/user/account.sock"
EXPECT_SCRIPT = "/home/user/health_check.exp"
MONITOR_SCRIPT = "/home/user/monitor.sh"
HEALTH_LOG = "/home/user/health.log"

def test_daemon_files_exist():
    """Verify that the C file and compiled binary exist and are correct."""
    assert os.path.isfile(DAEMON_C), f"C source file {DAEMON_C} is missing."
    assert os.path.isfile(DAEMON_BIN), f"Compiled binary {DAEMON_BIN} is missing."
    st = os.stat(DAEMON_BIN)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {DAEMON_BIN} is not executable."

def test_daemon_running():
    """Verify that the daemon is currently running and socket exists."""
    assert os.path.isfile(PID_FILE), f"PID file {PID_FILE} is missing."
    with open(PID_FILE, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file {PID_FILE} does not contain a valid PID."

    # Check if process is running
    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {PID_FILE} is not running.")

    assert os.path.exists(SOCK_FILE), f"Socket file {SOCK_FILE} is missing."
    st = os.stat(SOCK_FILE)
    assert stat.S_ISSOCK(st.st_mode), f"{SOCK_FILE} is not a socket."

def test_daemon_protocol():
    """Verify the daemon protocol over the Unix socket."""
    # Test wrong password
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(SOCK_FILE)
        data = s.recv(1024)
        assert data == b"PASSWD:\n", f"Expected 'PASSWD:\\n', got {data!r}"

        s.sendall(b"wrongpass\n")
        data = s.recv(1024)
        assert data == b"DENIED\n", f"Expected 'DENIED:\\n', got {data!r}"
    finally:
        s.close()

    # Test correct password and PING
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(SOCK_FILE)
        data = s.recv(1024)
        assert data == b"PASSWD:\n", f"Expected 'PASSWD:\\n', got {data!r}"

        s.sendall(b"adminpass\n")
        data = s.recv(1024)
        assert data == b"AUTH_OK\n", f"Expected 'AUTH_OK:\\n', got {data!r}"

        s.sendall(b"PING\n")
        data = s.recv(1024)
        assert data == b"PONG\n", f"Expected 'PONG:\\n', got {data!r}"
    finally:
        s.close()

def test_expect_script():
    """Verify the Expect script works and exits with 0."""
    assert os.path.isfile(EXPECT_SCRIPT), f"Expect script {EXPECT_SCRIPT} missing."
    result = subprocess.run(["expect", EXPECT_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Expect script failed with exit code {result.returncode}. Output: {result.stdout} {result.stderr}"

def test_monitor_script():
    """Verify the monitor script appends HEALTHY to the log."""
    assert os.path.isfile(MONITOR_SCRIPT), f"Monitor script {MONITOR_SCRIPT} missing."

    lines_before = []
    if os.path.isfile(HEALTH_LOG):
        with open(HEALTH_LOG, "r") as f:
            lines_before = f.readlines()

    result = subprocess.run(["bash", MONITOR_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Monitor script failed with exit code {result.returncode}."

    assert os.path.isfile(HEALTH_LOG), f"Health log {HEALTH_LOG} was not created."
    with open(HEALTH_LOG, "r") as f:
        lines_after = f.readlines()

    assert len(lines_after) == len(lines_before) + 1, "Monitor script did not append exactly one line to the log."
    assert lines_after[-1].strip() == "HEALTHY", f"Expected 'HEALTHY' in log, got {lines_after[-1].strip()!r}"

def test_service_script():
    """Verify the service script can stop and start the daemon cleanly."""
    assert os.path.isfile(SERVICE_SH), f"Service script {SERVICE_SH} missing."

    # Stop the service
    subprocess.run(["bash", SERVICE_SH, "stop"], check=True)
    time.sleep(0.5)

    assert not os.path.exists(PID_FILE), f"PID file {PID_FILE} should be deleted after stop."
    assert not os.path.exists(SOCK_FILE), f"Socket file {SOCK_FILE} should be deleted after stop."

    # Start the service
    subprocess.run(["bash", SERVICE_SH, "start"], check=True)
    time.sleep(0.5)

    assert os.path.isfile(PID_FILE), f"PID file {PID_FILE} should be created after start."
    assert os.path.exists(SOCK_FILE), f"Socket file {SOCK_FILE} should be created after start."