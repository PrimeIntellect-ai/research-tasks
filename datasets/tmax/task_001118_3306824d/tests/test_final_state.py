# test_final_state.py

import os
import socket
import subprocess
import requests
import time
import pytest
import tomli # Using standard library where possible, but tomli is needed for toml if python < 3.11, wait, I can just read text or use `tomllib` if Python 3.11+. Let's just read text to be safe, or check for tomllib.
import json

def test_directories_and_symlink():
    """Verify that the required directories and symlink exist."""
    assert os.path.islink("/app/current"), "/app/current must be a symbolic link."
    assert os.readlink("/app/current") == "/app/edge-proxy-1.2.0", "/app/current must point to /app/edge-proxy-1.2.0"

    assert os.path.isdir("/app/etc"), "/app/etc directory must exist."
    assert os.path.isdir("/app/var/log"), "/app/var/log directory must exist."

def test_configuration_file():
    """Verify the configuration file exists and has correct contents."""
    config_path = "/app/etc/edge-proxy.toml"
    assert os.path.isfile(config_path), f"{config_path} must exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "http_port = 9090" in content
    assert "tcp_port = 9091" in content
    assert 'control_token = "edge-init-token-8842"' in content

def test_systemd_service_file():
    """Verify the systemd user service file is correctly configured."""
    service_path = "/home/user/.config/systemd/user/edge-proxy.service"
    assert os.path.isfile(service_path), f"Service file {service_path} must exist."

    with open(service_path, "r") as f:
        content = f.read()

    assert "/app/current/target/release/edge-proxy" in content, "ExecStart must point to the release binary."
    assert "TZ=Asia/Tokyo" in content, "TZ environment variable must be set to Asia/Tokyo."
    assert "LANG=en_US.UTF-8" in content, "LANG environment variable must be set to en_US.UTF-8."
    assert "/app/var/log/edge-proxy.log" in content, "StandardOutput/Error must be redirected to /app/var/log/edge-proxy.log"
    assert "/app/current" in content, "WorkingDirectory must be /app/current"

def test_service_running_and_enabled():
    """Verify that the edge-proxy service is running and enabled."""
    # Check if enabled
    try:
        subprocess.run(
            ["systemctl", "--user", "is-enabled", "edge-proxy.service"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ, XDG_RUNTIME_DIR="/run/user/1000")
        )
    except subprocess.CalledProcessError:
        pytest.fail("edge-proxy.service is not enabled.")

    # Check if active
    try:
        subprocess.run(
            ["systemctl", "--user", "is-active", "edge-proxy.service"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ, XDG_RUNTIME_DIR="/run/user/1000")
        )
    except subprocess.CalledProcessError:
        pytest.fail("edge-proxy.service is not running.")

def test_http_endpoint():
    """Verify the HTTP health endpoint returns the correct JSON."""
    url = "http://127.0.0.1:9090/health"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        data = response.json()
        assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
        assert data.get("timezone") == "Asia/Tokyo", f"Expected timezone 'Asia/Tokyo', got {data.get('timezone')}"
        assert data.get("locale") == "en_US.UTF-8", f"Expected locale 'en_US.UTF-8', got {data.get('locale')}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

def test_tcp_endpoint():
    """Verify the TCP control endpoint accepts AUTH and responds to PING."""
    host = "127.0.0.1"
    port = 9091

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            # Send AUTH and PING
            sock.sendall(b"AUTH edge-init-token-8842\nPING\n")

            # Read response
            response = sock.recv(1024).decode("utf-8")
            assert "PONG" in response, f"Expected 'PONG' in response, got {response!r}"
    except Exception as e:
        pytest.fail(f"TCP request failed: {e}")