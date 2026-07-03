# test_final_state.py

import os
import socket
import requests
import pytest

def test_binary_exists():
    binary_path = "/app/go-numcalc-v1.2.3/numcalc"
    assert os.path.isfile(binary_path), f"Expected compiled binary at {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The file at {binary_path} is not executable."

def test_http_health_check():
    try:
        response = requests.get("http://localhost:8081/health", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP health check at localhost:8081: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("status") == "ok", f"Expected JSON {{'status': 'ok'}}, got {data}"

def test_tcp_protocol():
    try:
        s = socket.create_connection(("localhost", 8080), timeout=5)
    except socket.error as e:
        pytest.fail(f"Failed to connect to TCP service at localhost:8080: {e}")

    with s:
        # Helper to send and read a line
        def send_and_receive(msg: str) -> str:
            s.sendall(msg.encode('utf-8'))
            f = s.makefile('r', encoding='utf-8')
            return f.readline()

        # 1. Auth
        auth_resp = send_and_receive("AUTH calc_secure_99\n")
        assert auth_resp.strip() == "OK", f"Expected 'OK' after AUTH, got {repr(auth_resp)}"

        # 2. Eval
        eval_resp = send_and_receive("EVAL 5 + 5\n")
        assert eval_resp.strip() == "RESULT 10", f"Expected 'RESULT 10' after EVAL 5 + 5, got {repr(eval_resp)}"

        # 3. Concurrent PI
        pi_resp = send_and_receive("CONCURRENT_PI 1000\n")
        assert pi_resp.strip() == "RESULT 3.141", f"Expected 'RESULT 3.141' after CONCURRENT_PI 1000, got {repr(pi_resp)}"