# test_final_state.py

import os
import socket
import urllib.request
import urllib.error
import pytest

def test_ssh_tunnel_active():
    """Test if the SSH tunnel is forwarding port 9090 to the mock API."""
    try:
        response = urllib.request.urlopen("http://127.0.0.1:9090/", timeout=2)
        data = response.read()
        assert b"SECRET_UPSTREAM_DATA" in data, "Port 9090 did not return the expected upstream data."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to tunneled port 9090: {e}")

def test_bash_profile_env_var():
    """Test if the environment variable is exported in .bash_profile."""
    bash_profile_path = "/home/user/.bash_profile"
    assert os.path.exists(bash_profile_path), f"File {bash_profile_path} does not exist."

    with open(bash_profile_path, "r") as f:
        content = f.read()

    expected_export = "export TUNNELED_API_URL=http://127.0.0.1:9090"
    assert expected_export in content, f"'{expected_export}' not found in {bash_profile_path}."

def test_backend_script_fixed():
    """Test if the backend script was modified to use the correct socket path."""
    app_path = "/home/user/backend/app.py"
    assert os.path.exists(app_path), f"Backend script missing at {app_path}"

    with open(app_path, "r") as f:
        content = f.read()

    assert "/home/user/backend.sock" in content, "Backend script does not contain the new socket path."
    assert "/var/run/backend.sock" not in content, "Backend script still contains the broken socket path."

def test_unix_socket_running():
    """Test if the backend application is running and serving over the Unix socket."""
    sock_path = "/home/user/backend.sock"
    assert os.path.exists(sock_path), f"Unix socket {sock_path} does not exist. Is the backend running?"

    # Try connecting to the unix socket and sending a simple HTTP GET
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(2)
        client.connect(sock_path)
        client.sendall(b"GET / HTTP/1.0\r\n\r\n")

        response = b""
        while True:
            chunk = client.recv(1024)
            if not chunk:
                break
            response += chunk
        client.close()

        assert b"SECRET_UPSTREAM_DATA" in response, "Unix socket response did not contain the expected upstream data."
    except Exception as e:
        pytest.fail(f"Failed to communicate with Unix socket: {e}")

def test_dockerfile_contents():
    """Test if the Dockerfile is created and contains the required directives."""
    dockerfile_path = "/home/user/backend/Dockerfile"
    assert os.path.exists(dockerfile_path), f"Dockerfile missing at {dockerfile_path}"

    with open(dockerfile_path, "r") as f:
        content = f.read()

    assert "FROM python:3.10-slim" in content, "Dockerfile does not use 'python:3.10-slim' as the base image."
    assert "app.py" in content, "Dockerfile does not mention 'app.py'."
    assert "/app" in content, "Dockerfile does not mention the '/app' directory."
    assert "python" in content, "Dockerfile does not set python as part of the command."

def test_result_log():
    """Test if the verification script successfully wrote the result to result.log."""
    log_path = "/home/user/result.log"
    assert os.path.exists(log_path), f"Log file missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SECRET_UPSTREAM_DATA" in content, f"Log file {log_path} does not contain the expected data."