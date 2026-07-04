# test_final_state.py

import os
import socket
import pytest

EXPECTED_TOKEN = "8f9b2a7c-4e1d-48a5-9032-abcdef123456"

def test_git_hook_exists_and_executable():
    """Test that the post-receive hook exists and is executable."""
    hook_path = "/home/user/deploy.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"The post-receive hook does not exist at {hook_path}"
    assert os.path.isfile(hook_path), f"The path {hook_path} is not a file"
    assert os.access(hook_path, os.X_OK), f"The post-receive hook at {hook_path} is not executable"

def test_tcp_server_response():
    """Test that the TCP server is running on port 9090 and returns the correct token."""
    host = '127.0.0.1'
    port = 9090

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))

            # Read data from the server
            data = s.recv(1024).decode('utf-8')

            # The server should close the connection after sending the token
            # Check if the token is correct (strip whitespace/newlines for robust comparison)
            assert data.strip() == EXPECTED_TOKEN, f"Expected token '{EXPECTED_TOKEN}', but received '{data.strip()}'"

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to the server at {host}:{port}. Is it running?")
    except socket.timeout:
        pytest.fail(f"Connection to {host}:{port} timed out.")
    except Exception as e:
        pytest.fail(f"An error occurred while connecting to the server: {e}")

def test_deployed_files_exist():
    """Test that the deployed service directory and compiled binary exist."""
    deployed_dir = "/home/user/deployed_service"
    binary_path = os.path.join(deployed_dir, "server_bin")

    assert os.path.exists(deployed_dir), f"Deployed service directory {deployed_dir} does not exist"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist"
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable"

def test_workspace_files_exist():
    """Test that the workspace directory and source file exist."""
    workspace_dir = "/home/user/workspace"
    source_path = os.path.join(workspace_dir, "server.c")

    assert os.path.exists(workspace_dir), f"Workspace directory {workspace_dir} does not exist"
    assert os.path.exists(source_path), f"Source file {source_path} does not exist"