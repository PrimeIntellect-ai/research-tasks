# test_final_state.py
import os
import random
import socket
import json
import pytest
import requests
import concurrent.futures

def expected_result(a, b):
    return 42.0 * (a * b) / (a + b + 0.001)

def check_http(a, b):
    url = "http://127.0.0.1:8080/compute"
    payload = {"a": a, "b": b}
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        assert "result" in data, "HTTP response missing 'result' key"
        result = float(data["result"])
        expected = expected_result(a, b)
        assert abs(result - expected) < 1e-5, f"HTTP result mismatch for {a}, {b}: expected {expected}, got {result}"
        return True
    except Exception as e:
        return str(e)

def check_tcp(a, b):
    try:
        with socket.create_connection(("127.0.0.1", 8081), timeout=5) as sock:
            msg = f"{a},{b}\n"
            sock.sendall(msg.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8').strip()
            result = float(response)
            expected = expected_result(a, b)
            assert abs(result - expected) < 1e-5, f"TCP result mismatch for {a}, {b}: expected {expected}, got {result}"
            return True
    except Exception as e:
        return str(e)

def test_regression_test_script_exists():
    path = "/home/user/regression_test.py"
    assert os.path.exists(path), f"Missing regression test script at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_http_service_concurrency():
    inputs = [(random.uniform(1.0, 100.0), random.uniform(1.0, 100.0)) for _ in range(50)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_http, a, b) for a, b in inputs]

        errors = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not True:
                errors.append(res)

        assert not errors, f"HTTP concurrency test failed with errors: {errors[:5]}"

def test_tcp_service_concurrency():
    inputs = [(random.uniform(1.0, 100.0), random.uniform(1.0, 100.0)) for _ in range(50)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_tcp, a, b) for a, b in inputs]

        errors = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not True:
                errors.append(res)

        assert not errors, f"TCP concurrency test failed with errors: {errors[:5]}"