# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import pytest

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "size 10" in content or "size 10b" in content or "size=10" in content.replace(" ", ""), "Missing 'size 10' directive in logrotate.conf"
    assert "rotate 3" in content, "Missing 'rotate 3' directive in logrotate.conf"
    assert "compress" in content, "Missing 'compress' directive in logrotate.conf"
    assert "missingok" in content, "Missing 'missingok' directive in logrotate.conf"
    assert "nomail" in content, "Missing 'nomail' directive in logrotate.conf"

def test_supervisor_script():
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read()

    assert "smtp_monitor" in content, "Supervisor script does not seem to call the smtp_monitor binary."
    assert "sleep 1" in content, "Supervisor script does not seem to sleep for 1 second on failure."

def test_rust_project_builds():
    project_dir = "/home/user/smtp_monitor"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} is missing."
    assert os.path.isfile(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml is missing."
    assert os.path.isfile(os.path.join(project_dir, "src", "main.rs")), "src/main.rs is missing."

    result = subprocess.run(["cargo", "build"], cwd=project_dir, capture_output=True)
    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr.decode()}"

def start_dummy_server(port, stop_event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.settimeout(0.5)
        s.listen(1)
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                conn.close()
                break
            except socket.timeout:
                continue

def test_rust_logic_and_side_effects():
    binary_path = "/home/user/smtp_monitor/target/debug/smtp_monitor"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}."

    aliases_path = "/home/user/mail_aliases.txt"
    log_path = "/home/user/logs/smtp_monitor.log"

    # Reset files for clean test
    with open(aliases_path, "w") as f:
        f.write("sysadmins: root, admin\nnet-admins: bob, charlie\n")
    if os.path.exists(log_path):
        os.remove(log_path)

    # Test 1: Failure case (no server listening)
    result = subprocess.run([binary_path], capture_output=True)
    assert result.returncode == 1, "Binary should exit with status 1 when all connections fail."

    assert os.path.isfile(log_path), "Log file was not created."
    with open(log_path, "r") as f:
        logs = f.read().splitlines()
    assert len(logs) == 3, "Should have made exactly 3 attempts."
    assert all(l == "CONNECT_FAIL" for l in logs), "Logs should contain CONNECT_FAIL for failed attempts."

    # Check mail_aliases.txt modification
    with open(aliases_path, "r") as f:
        aliases_content = f.read()
    assert "net-admins: bob, charlie, alice" in aliases_content or "alice" in aliases_content.split("net-admins:")[1].split("\n")[0], "User 'alice' was not properly appended to net-admins."

    # Reset log file for success test
    os.remove(log_path)

    # Test 2: Success case (server listening)
    stop_event = threading.Event()
    server_thread = threading.Thread(target=start_dummy_server, args=(2525, stop_event))
    server_thread.start()

    try:
        time.sleep(0.2) # wait for server to bind
        result = subprocess.run([binary_path], capture_output=True)
        assert result.returncode == 0, "Binary should exit with status 0 when at least one connection succeeds."

        with open(log_path, "r") as f:
            logs = f.read().splitlines()
        assert "CONNECT_OK" in logs, "Logs should contain CONNECT_OK for successful attempts."
    finally:
        stop_event.set()
        server_thread.join()