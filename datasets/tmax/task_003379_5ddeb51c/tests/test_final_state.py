# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_test_output():
    """Verify that deploy_test.txt exists and contains the correct output."""
    path = "/home/user/deploy_test.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "Deploy v2 OK", f"Content of {path} was '{content}', expected 'Deploy v2 OK'."

def test_nginx_running():
    """Verify that Nginx is running and loaded the specific configuration file."""
    result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to execute ps command."

    # Check if nginx is running with the correct config
    processes = result.stdout.splitlines()
    nginx_running = any("nginx" in line and "/home/user/nginx/nginx.conf" in line for line in processes)
    assert nginx_running, "Nginx is not running or not loaded with /home/user/nginx/nginx.conf."

def test_ssh_tunnel_running():
    """Verify that the SSH tunnel process is running with the correct port forwarding."""
    result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to execute ps command."

    # Check for the specific SSH tunnel arguments
    processes = result.stdout.splitlines()
    tunnel_running = any("8888:127.0.0.1:8080" in line for line in processes)
    assert tunnel_running, "SSH tunnel process identifiable by '8888:127.0.0.1:8080' is not running."

def test_rust_backend_source():
    """Verify that the Rust backend source code contains the required strings."""
    path = "/home/user/backend/src/main.rs"
    assert os.path.isfile(path), f"Rust source file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "UnixListener::bind" in content, f"Rust source in {path} is missing 'UnixListener::bind'."
    assert "Deploy v2 OK" in content, f"Rust source in {path} is missing the string 'Deploy v2 OK'."