# test_final_state.py

import os
import socket
import subprocess
import re

def test_symlink_and_directories():
    """Verify the directory structure, compiled binary, and symlink."""
    assert os.path.isdir("/home/user/app/bin"), "/home/user/app/bin directory is missing."
    assert os.path.isdir("/home/user/app/active"), "/home/user/app/active directory is missing."
    assert os.path.isdir("/home/user/app/logs"), "/home/user/app/logs directory is missing."

    bin_path = "/home/user/app/bin/migrator"
    symlink_path = "/home/user/app/active/migrator"

    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == bin_path, f"Symlink {symlink_path} does not point to {bin_path}."

def test_systemd_service():
    """Verify the systemd service file contains the correct directives."""
    service_path = "/home/user/.config/systemd/user/migrator.service"
    assert os.path.isfile(service_path), f"Systemd service file {service_path} is missing."

    with open(service_path, "r") as f:
        content = f.read()

    assert "ExecStart=/home/user/app/active/migrator" in content, "ExecStart directive is missing or incorrect."

    # Check Environment directives
    assert re.search(r"Environment=.*MIGRATION_PORT=9090", content), "MIGRATION_PORT environment variable not set correctly in service file."
    assert re.search(r"Environment=.*MIGRATION_LOG=/home/user/app/logs/migrator\.log", content), "MIGRATION_LOG environment variable not set correctly in service file."

def test_start_script():
    """Verify the start shell script exists and is executable."""
    script_path = "/home/user/app/start.sh"
    assert os.path.isfile(script_path), f"Startup script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Startup script {script_path} is not executable."

def test_service_running_and_pid():
    """Verify the PID file exists, matches a running process, and port 9090 is listening."""
    pid_file = "/home/user/app/migrator.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

    # Check if port 9090 is listening on 127.0.0.1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # If it connects, something is listening
        s.connect(("127.0.0.1", 9090))
        s.close()
    except ConnectionRefusedError:
        assert False, "No service is listening on 127.0.0.1:9090."

def test_log_output():
    """Verify the log file exists and contains the correct startup message."""
    log_path = "/home/user/app/logs/migrator.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "SERVICE_UP" in content, f"Log file {log_path} does not contain 'SERVICE_UP'."