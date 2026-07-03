# test_final_state.py

import os
import tarfile
import stat
import subprocess
import pytest

def test_backup_exists_and_valid():
    backup_path = "/home/user/migration/backup/src_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file missing: {backup_path}"

    with tarfile.open(backup_path, "r:gz") as tar:
        names = [os.path.basename(m.name) for m in tar.getmembers()]
        assert "server.c" in names, "server.c not found in the backup tarball"

def test_binary_and_process():
    binary_path = "/home/user/migration/bin/backend_daemon"
    pid_file = "/home/user/migration/daemon.pid"

    assert os.path.isfile(binary_path), f"Compiled binary missing: {binary_path}"
    assert os.path.isfile(pid_file), f"PID file missing: {pid_file}"

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running")

def test_socket_exists():
    socket_path = "/home/user/migration/socket/backend.sock"
    assert os.path.exists(socket_path), f"Socket missing: {socket_path}"
    mode = os.stat(socket_path).st_mode
    assert stat.S_ISSOCK(mode), f"{socket_path} is not a socket"

def test_proxy_response():
    response_file = "/home/user/migration/test_response.txt"
    assert os.path.isfile(response_file), f"Response file missing: {response_file}"

    with open(response_file, "r") as f:
        content = f.read()

    assert "Hello Server!" in content, "Response file does not contain 'Hello Server!'"

def test_monitoring_script_and_status():
    monitor_script = "/home/user/migration/monitor.sh"
    status_file = "/home/user/migration/status.txt"

    assert os.path.isfile(monitor_script), f"Monitor script missing: {monitor_script}"
    assert os.path.isfile(status_file), f"Status file missing: {status_file}"

    with open(status_file, "r") as f:
        status_content = f.read()

    assert "Log Active" in status_content, "Status file does not contain 'Log Active'"