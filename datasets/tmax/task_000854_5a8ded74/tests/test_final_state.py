# test_final_state.py

import socket
import requests
import pytest

def test_tcp_health_check():
    """Test the TCP health check endpoint."""
    host = "127.0.0.1"
    port = 9001
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
            assert data == b"PONG\n", f"Expected b'PONG\\n', got {data!r}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. Is the TCP health check service running?")
    except socket.timeout:
        pytest.fail(f"Connection to {host}:{port} timed out.")
    except Exception as e:
        pytest.fail(f"Failed to connect and communicate with TCP health check: {e}")

def test_http_process_hello():
    """Test the HTTP endpoint with 'hello'."""
    url = "http://127.0.0.1:8080/api/process"
    data = "hello"
    expected = "ifmmp"
    try:
        response = requests.post(url, data=data, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        assert response.text == expected, f"Expected response body {expected!r}, got {response.text!r}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Connection refused to {url}. Is Nginx running and configured correctly?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")
    except Exception as e:
        pytest.fail(f"Failed to make HTTP request: {e}")

def test_http_process_data_processing():
    """Test the HTTP endpoint with 'data processing'."""
    url = "http://127.0.0.1:8080/api/process"
    data = "data processing"
    expected = "ebub!qspdfttjoh"
    try:
        response = requests.post(url, data=data, timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
        assert response.text == expected, f"Expected response body {expected!r}, got {response.text!r}"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Connection refused to {url}. Is Nginx running and configured correctly?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")
    except Exception as e:
        pytest.fail(f"Failed to make HTTP request: {e}")