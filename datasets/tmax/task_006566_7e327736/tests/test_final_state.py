# test_final_state.py

import os
import stat
import socket
import subprocess
import pytest

def test_run_dir_permissions():
    """Check that /home/user/run exists and has 700 permissions."""
    dir_path = "/home/user/run"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    st = os.stat(dir_path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o700, f"Permissions for {dir_path} should be 700, but are {oct(mode)}."

def test_backend_c_updated():
    """Check that backend.c was updated with the correct socket path."""
    file_path = "/home/user/backend.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "/home/user/run/backend.sock" in content, "backend.c does not contain the updated socket path."

def test_backend_executable():
    """Check that backend was compiled and is executable."""
    exe_path = "/home/user/backend"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_supervisor_running():
    """Check that supervisor.sh exists, is executable, and is running."""
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Check if supervisor is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisor.sh"]).decode("utf-8").strip()
        assert output, "supervisor.sh process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("supervisor.sh process is not running (pgrep returned no results).")

def test_response_file():
    """Check that response.txt exists and contains 'ACK'."""
    file_path = "/home/user/response.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert "ACK" in content, f"response.txt does not contain 'ACK'. Found: {content}"

def test_socket_live():
    """Test that the backend socket is live and responds to a message."""
    sock_path = "/home/user/run/backend.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} does not exist."

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(sock_path)
        client.sendall(b"PING")
        response = client.recv(1024).decode("utf-8")
        assert "ACK" in response, f"Expected 'ACK' from socket, got {response}"
    except Exception as e:
        pytest.fail(f"Failed to communicate with socket {sock_path}: {e}")
    finally:
        client.close()