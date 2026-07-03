# test_final_state.py

import os
import sys
import json
import socket
import pytest
import requests
import pandas as pd
import numpy as np

def test_fast_corr_installed():
    """Verify that the fast_corr package was successfully installed and is importable."""
    try:
        import fast_corr
    except ImportError:
        pytest.fail("The fast_corr package is not installed or importable. Ensure setup.py was fixed and installed correctly.")

    # Test that it computes correlation
    x = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    y = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    try:
        corr = fast_corr.compute(x, y)
        assert isinstance(corr, float), "fast_corr.compute did not return a float."
    except Exception as e:
        pytest.fail(f"fast_corr.compute failed when called: {e}")

def test_tcp_health_service():
    """Verify the TCP health service on port 8081 responds to PING\\n with PONG\\n."""
    host = '127.0.0.1'
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
            response = data.decode('utf-8')
            assert response == "PONG\n", f"Expected 'PONG\\n', but got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"TCP connection refused on {host}:{port}. Is the health service running?")
    except socket.timeout:
        pytest.fail("TCP connection timed out waiting for a response.")
    except Exception as e:
        pytest.fail(f"TCP health service test failed: {e}")

def test_http_auth_missing():
    """Verify the HTTP REST API returns 401 Unauthorized when missing the Bearer token."""
    url = "http://127.0.0.1:8080/predict"
    payload = {"f2": 1.0, "f4": 1.0}

    try:
        response = requests.post(url, json=payload, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized when missing token, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("HTTP connection refused on port 8080. Is the API service running?")

def test_http_auth_incorrect():
    """Verify the HTTP REST API returns 401 Unauthorized with an incorrect Bearer token."""
    url = "http://127.0.0.1:8080/predict"
    payload = {"f2": 1.0, "f4": 1.0}
    headers = {"Authorization": "Bearer wrong_token"}

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized with incorrect token, got {response.status_code}"

def test_http_predict_valid():
    """Verify the HTTP REST API returns a valid prediction when provided the correct features and token."""
    url = "http://127.0.0.1:8080/predict"
    payload = {"f2": 0.5, "f4": -0.5}
    headers = {"Authorization": "Bearer research_token"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert "prediction" in data, f"Response JSON missing 'prediction' key. Got: {data}"
        assert isinstance(data["prediction"], (int, float)), "Prediction value must be a number."
    except requests.exceptions.ConnectionError:
        pytest.fail("HTTP connection refused on port 8080. Is the API service running?")
    except json.JSONDecodeError:
        pytest.fail(f"HTTP response was not valid JSON. Response text: {response.text}")