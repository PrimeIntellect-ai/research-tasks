# test_final_state.py

import os
import json
import socket
import requests
import pytest

def test_libminiscript_compiled():
    so_path = "/app/vendor/miniscript/libminiscript.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled."

def test_benchmark_files_exist():
    assert os.path.isfile("/app/benchmark.py"), "/app/benchmark.py is missing."

    result_path = "/app/bench_result.txt"
    assert os.path.isfile(result_path), f"{result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val >= 0, "Benchmark result should be a positive float."
    except ValueError:
        pytest.fail(f"Contents of {result_path} cannot be parsed as a float: {content}")

def test_http_protocol_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/evaluate"
    payload = {"rule": "return len(input) > 5;", "payload": "abcdef"}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on 8080: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_http_protocol_authorized():
    url = "http://127.0.0.1:8080/api/v1/evaluate"
    headers = {"Authorization": "Bearer sec-token-999"}
    payload = {"rule": "return len(input) > 5;", "payload": "abcdef"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on 8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Missing 'result' in JSON response: {data}"
    # The truth specifies expecting 1 for this input
    assert data["result"] == 1, f"Expected result to be 1, got {data['result']}"

def test_tcp_protocol():
    host = "127.0.0.1"
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            message = b"return input == 'admin';|admin\n"
            sock.sendall(message)

            response = b""
            while b"\n" not in response:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                response += chunk

    except (socket.error, socket.timeout) as e:
        pytest.fail(f"Failed to connect or communicate with TCP server on {port}: {e}")

    assert response.decode('utf-8') == "1\n", f"Expected '1\\n' from TCP server, got {response!r}"