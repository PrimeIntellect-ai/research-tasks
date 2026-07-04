# test_final_state.py

import os
import stat
import subprocess
import requests
import pytest

def test_gateway_daemon_built():
    """Verify that the gateway_daemon executable was built."""
    path = "/app/microservice-gateway-1.2/gateway_daemon"
    assert os.path.isfile(path), f"Executable {path} not found. Did you fix the Makefile and compile?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_setup_env_script_exists_and_executable():
    """Verify setup_env.sh exists and is executable."""
    path = "/home/user/setup_env.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_bashrc_contains_variables():
    """Verify .bashrc contains the required environment variables."""
    path = "/home/user/.bashrc"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "GATEWAY_PORT=9000" in content, "GATEWAY_PORT=9000 not found in .bashrc"
    assert "HTTP_PORT=9001" in content, "HTTP_PORT=9001 not found in .bashrc"
    assert "GATEWAY_TOKEN=secure-micro-token" in content, "GATEWAY_TOKEN=secure-micro-token not found in .bashrc"

def test_enable_http_exp_exists():
    """Verify enable_http.exp exists."""
    path = "/home/user/enable_http.exp"
    assert os.path.isfile(path), f"{path} does not exist."

def test_ssh_tunnel_listening():
    """Verify that a process is listening on 127.0.0.1:8080."""
    try:
        output = subprocess.check_output(["ss", "-tln"], text=True)
        assert ":8080" in output, "No service is listening on port 8080. SSH tunnel might not be running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ss command.")

def test_gateway_http_endpoint():
    """Verify the microservice gateway is active and fully functional via the SSH tunnel."""
    url = "http://127.0.0.1:8080/"
    headers = {
        "Authorization": "Bearer secure-micro-token"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the gateway at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    assert "Gateway Active" in response.text, f"Expected 'Gateway Active' in response body, got: {response.text}"