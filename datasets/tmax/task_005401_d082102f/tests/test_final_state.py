# test_final_state.py

import os
import socket
import requests
import pytest

def test_service_pid_exists_and_running():
    pid_file = "/app/service.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist. The service PID must be written here."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"{pid_file} does not contain a valid numeric PID. Found: {pid_str}"

    pid = int(pid_str)
    assert os.path.exists(f"/proc/{pid}"), f"Process with PID {pid} is not running."

def test_http_endpoint():
    url = "http://127.0.0.1:8080/process"
    payload = {"input": 10}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP endpoint at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert data.get("status") == "success", f"Expected 'status' to be 'success', got {data.get('status')}"
    assert data.get("output") == 100, f"Expected 'output' to be 100, got {data.get('output')}"

def test_tcp_endpoint():
    host = "127.0.0.1"
    port = 8081

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP endpoint at {host}:{port}. Error: {e}")

    try:
        s.sendall(b"HEARTBEAT\n")
        response = s.recv(1024)
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP endpoint. Error: {e}")
    finally:
        s.close()

    assert response == b"ALIVE\n", f"Expected response b'ALIVE\\n', got {response!r}"

def test_cmake_configuration_fixed():
    cmake_path = "/app/fastalgo/CMakeLists.txt"
    assert os.path.exists(cmake_path), f"CMakeLists.txt missing at {cmake_path}"

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "target_link_libraries" in content, "CMakeLists.txt is missing the 'target_link_libraries' directive to link libalgo.so."