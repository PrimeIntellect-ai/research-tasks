# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import pytest

def test_compiled_binary_exists():
    binary_path = "/home/user/disk_monitor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_mail_offline_behavior():
    # Ensure port 2525 is free by trying to bind to it, or just assume it's free.
    # Run the wrapper script
    result = subprocess.run(["bash", "/home/user/run_monitor.sh"], capture_output=True)

    # Check that it exited with status 1
    assert result.returncode == 1, "Script should exit with status 1 when mail is offline."

    log_path = "/home/user/monitor_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "Mail offline", f"Log file content incorrect. Expected 'Mail offline', got '{content}'."

def dummy_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 2525))
    server_socket.listen(1)
    try:
        # Accept one connection then close, or just wait until stopped
        server_socket.settimeout(5.0)
        conn, _ = server_socket.accept()
        conn.close()
    except socket.timeout:
        pass
    finally:
        server_socket.close()

def test_normal_run_behavior():
    # Clean up previous state
    log_path = "/home/user/monitor_status.log"
    email_path = "/home/user/alerts/email.txt"
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(email_path):
        os.remove(email_path)

    # Start dummy server on port 2525
    server_thread = threading.Thread(target=dummy_server)
    server_thread.daemon = True
    server_thread.start()

    # Give the server a moment to start listening
    time.sleep(0.5)

    # Run the wrapper script
    result = subprocess.run(["bash", "/home/user/run_monitor.sh"], capture_output=True)

    # Wait for server thread
    server_thread.join(timeout=1.0)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created on successful run."
    with open(log_path, "r") as f:
        log_content = f.read().strip()
    assert log_content == "Success", f"Log file content incorrect. Expected 'Success', got '{log_content}'."

    assert os.path.isdir("/home/user/alerts"), "Directory /home/user/alerts was not created."
    assert os.path.isfile(email_path), f"Email alert file {email_path} was not created."

    with open(email_path, "r") as f:
        email_content = f.read().strip()
    assert email_content == "QUOTA EXCEEDED", f"Email file content incorrect. Expected 'QUOTA EXCEEDED', got '{email_content}'."