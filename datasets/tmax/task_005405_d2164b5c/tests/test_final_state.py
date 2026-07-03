# test_final_state.py

import os
import socket
import time
import signal
import requests
import pytest

HTTP_PORT = 9080
TCP_PORT = 9081
SECRET = "BGP456"

def test_directory_structure():
    base_dir = "/home/user/diag_service"
    dirs = [
        f"{base_dir}/bin",
        f"{base_dir}/logs",
        f"{base_dir}/run"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist"

    symlink_path = f"{base_dir}/current_logs"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    assert os.readlink(symlink_path) == f"{base_dir}/logs", f"Symlink {symlink_path} does not point to {base_dir}/logs"

def test_http_server():
    url = f"http://127.0.0.1:{HTTP_PORT}/status"

    # Test 1: Auth Success
    headers = {"X-Diag-Secret": SECRET}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    try:
        data = response.json()
        assert data == {"status": "UP"}, f"Expected JSON {{'status': 'UP'}}, got {data}"
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    # Test 2: Auth Failure
    headers_wrong = {"X-Diag-Secret": "WRONG"}
    response_wrong = requests.get(url, headers=headers_wrong, timeout=2)
    assert response_wrong.status_code == 401, f"Expected status 401 for wrong secret, got {response_wrong.status_code}"

def test_tcp_server():
    # Test 1: Auth Success
    try:
        s = socket.create_connection(("127.0.0.1", TCP_PORT), timeout=2)
        s.sendall(f"AUTH {SECRET}\n".encode())
        time.sleep(0.1)
        s.sendall(b"PING\n")
        data = s.recv(1024).decode()
        assert "PING" in data, f"Expected 'PING' in response, got {data}"
        s.close()
    except Exception as e:
        pytest.fail(f"TCP Auth Success test failed: {e}")

    # Test 2: Auth Failure
    try:
        s2 = socket.create_connection(("127.0.0.1", TCP_PORT), timeout=2)
        s2.sendall(b"AUTH INVALID\n")
        time.sleep(0.1)
        s2.sendall(b"PING\n")
        data = s2.recv(1024)
        assert data == b"", f"Expected connection to be dropped, but received {data}"
        s2.close()
    except (ConnectionResetError, BrokenPipeError):
        pass # Expected
    except Exception as e:
        pytest.fail(f"TCP Auth Failure test failed: {e}")

def test_logging_and_supervisor():
    base_dir = "/home/user/diag_service"
    access_log = f"{base_dir}/logs/access.log"
    service_log = f"{base_dir}/logs/service.log"
    pid_file = f"{base_dir}/run/service.pid"

    assert os.path.isfile(access_log), f"{access_log} does not exist"
    assert os.path.getsize(access_log) > 0, f"{access_log} is empty"

    assert os.path.isfile(service_log), f"{service_log} does not exist"

    assert os.path.isfile(pid_file), f"{pid_file} does not exist"
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    try:
        pid = int(pid_str)
    except ValueError:
        pytest.fail(f"PID file {pid_file} does not contain a valid integer: {pid_str}")

    # Test supervisor restart policy
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass # Process might already be dead, but let's check if it restarts

    # Wait for restart
    time.sleep(2)

    # Verify ports are active again
    try:
        response = requests.get(f"http://127.0.0.1:{HTTP_PORT}/status", headers={"X-Diag-Secret": SECRET}, timeout=2)
        assert response.status_code == 200, "HTTP server did not restart properly"
    except requests.RequestException:
        pytest.fail("HTTP server did not restart after being killed")

    try:
        s = socket.create_connection(("127.0.0.1", TCP_PORT), timeout=2)
        s.close()
    except Exception:
        pytest.fail("TCP server did not restart after being killed")