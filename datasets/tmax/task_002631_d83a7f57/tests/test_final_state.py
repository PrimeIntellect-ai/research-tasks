# test_final_state.py

import os
import socket
import pytest
import requests

def test_configure_exp_exists():
    """Check if the Expect script was created."""
    exp_path = "/home/user/configure.exp"
    assert os.path.isfile(exp_path), f"Missing Expect script at {exp_path}"

def test_router_cfg_exists_and_content():
    """Check if the router.cfg was generated with correct content."""
    cfg_path = "/home/user/router.cfg"
    assert os.path.isfile(cfg_path), f"Missing configuration file at {cfg_path}"
    with open(cfg_path, 'r') as f:
        content = f.read().strip()
    assert content == "SUCCESS: 4011,4022,4033", f"Incorrect content in {cfg_path}: {content}"

def test_gateway_sh_exists():
    """Check if the gateway script was created."""
    sh_path = "/home/user/gateway.sh"
    assert os.path.isfile(sh_path), f"Missing gateway script at {sh_path}"

def test_gateway_pid_exists():
    """Check if the gateway PID file was created."""
    pid_path = "/home/user/gateway.pid"
    assert os.path.isfile(pid_path), f"Missing gateway PID file at {pid_path}"
    with open(pid_path, 'r') as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file does not contain a valid PID: {pid}"
    # Check if process is running
    assert os.path.exists(f"/proc/{pid}"), f"Process with PID {pid} is not running"

def test_http_gateway_status():
    """Check if the HTTP gateway responds correctly on port 8888."""
    url = "http://127.0.0.1:8888/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    expected_body = "SUCCESS: 4011,4022,4033"
    assert expected_body in response.text, f"Expected body to contain '{expected_body}', got '{response.text}'"

def test_tcp_gateway_sync_ack():
    """Check if the TCP gateway responds correctly on port 8889."""
    host = "127.0.0.1"
    port = 8889

    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
    except Exception as e:
        pytest.fail(f"TCP connection to {host}:{port} failed: {e}")

    response_str = data.decode('utf-8')
    assert response_str == "SYNC_ACK\n", f"Expected TCP response 'SYNC_ACK\\n', got {repr(response_str)}"