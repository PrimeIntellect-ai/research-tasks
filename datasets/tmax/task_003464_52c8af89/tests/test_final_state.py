# test_final_state.py

import os
import stat
import socket
import requests
import pytest
import time

def test_git_setup():
    repo_dir = "/home/user/monitor.git"
    hook_path = os.path.join(repo_dir, "hooks/post-receive")
    deploy_dir = "/home/user/deploy"

    assert os.path.isdir(repo_dir), f"Bare git repository not found at {repo_dir}"
    assert os.path.isdir(deploy_dir), f"Deploy directory not found at {deploy_dir}"
    assert os.path.exists(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook is not executable"

def test_qemu_qmp_socket():
    sock_path = "/tmp/legacy_qmp.sock"
    assert os.path.exists(sock_path), f"QMP socket not found at {sock_path}. Is QEMU running?"
    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"Path {sock_path} is not a socket"

def test_raw_tcp_service():
    host = "127.0.0.1"
    port = 8040
    expected_output = "HEARTBEAT_OK_78291"

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\n")
            response = s.recv(4096).decode("utf-8")
            assert expected_output in response, f"Expected '{expected_output}' in response, got: {response}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to Raw TCP service on {host}:{port}")
    except socket.timeout:
        pytest.fail(f"Timeout connecting to or reading from Raw TCP service on {host}:{port}")

def test_http_service():
    url = "http://127.0.0.1:8080/uptime"
    expected_output = "HEARTBEAT_OK_78291"

    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        assert expected_output in response.text, f"Expected '{expected_output}' in HTTP response body, got: {response.text}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to HTTP service at {url}")
    except requests.exceptions.Timeout:
        pytest.fail(f"Timeout connecting to HTTP service at {url}")