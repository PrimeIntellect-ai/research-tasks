# test_final_state.py

import os
import subprocess
import socket
import threading
import pytest

def get_total_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_rust_source_exists():
    assert os.path.exists("/home/user/quota_monitor.rs"), "Rust source file /home/user/quota_monitor.rs does not exist."

def test_rust_binary_exists_and_executable():
    binary_path = "/home/user/quota_monitor"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

def test_connection_failure_branch():
    binary_path = "/home/user/quota_monitor"
    tunnel_cmd_path = "/home/user/tunnel_cmd.sh"

    # Ensure port 5555 is not bound
    # Run the binary
    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {binary_path} failed with return code {result.returncode}."

    # Check if tunnel_cmd.sh was created
    assert os.path.exists(tunnel_cmd_path), f"{tunnel_cmd_path} was not created when connection failed."

    with open(tunnel_cmd_path, "r") as f:
        content = f.read().strip()

    expected_cmd = "ssh -N -f -L 5555:metrics.internal:80 admin@bastion.host"
    assert content == expected_cmd, f"Expected '{expected_cmd}' in {tunnel_cmd_path}, but got '{content}'."

    # Clean up for the next test
    os.remove(tunnel_cmd_path)

def test_connection_success_branch():
    binary_path = "/home/user/quota_monitor"
    data_dir = "/home/user/user_data"

    expected_size = get_total_size(data_dir)
    expected_msg = f"QUOTA_EXCEEDED:{expected_size}"

    received_data = []

    def mock_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 5555))
            s.listen(1)
            s.settimeout(5)
            try:
                conn, _ = s.accept()
                with conn:
                    data = conn.recv(1024)
                    received_data.append(data.decode('utf-8'))
            except socket.timeout:
                pass

    server_thread = threading.Thread(target=mock_server)
    server_thread.start()

    # Give the server a moment to start listening
    import time
    time.sleep(0.5)

    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {binary_path} failed with return code {result.returncode}."

    server_thread.join()

    assert len(received_data) > 0, "No data was received by the mock server on port 5555."
    assert received_data[0] == expected_msg, f"Expected to receive '{expected_msg}', but got '{received_data[0]}'."