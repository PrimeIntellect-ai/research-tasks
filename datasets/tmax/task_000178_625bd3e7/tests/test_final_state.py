# test_final_state.py
import socket
import requests
import pytest

HTTP_URL = "http://127.0.0.1:8080/admin_check"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8081

def test_http_service_success():
    headers = {"X-Backdoor-Auth": "falcon99"}
    cookies = {"LegacySessionCookie": "anyvalue"}

    try:
        response = requests.get(HTTP_URL, headers=headers, cookies=cookies, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {HTTP_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail("Expected JSON response but failed to parse it.")

    assert json_data == {"access": "granted"}, f"Expected JSON {{'access': 'granted'}}, got {json_data}"

def test_http_service_missing_header():
    cookies = {"LegacySessionCookie": "anyvalue"}

    try:
        response = requests.get(HTTP_URL, cookies=cookies, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {HTTP_URL}: {e}")

    assert response.status_code == 403, f"Expected status code 403 when header is missing, got {response.status_code}"

def test_http_service_wrong_header():
    headers = {"X-Backdoor-Auth": "wrongpass"}
    cookies = {"LegacySessionCookie": "anyvalue"}

    try:
        response = requests.get(HTTP_URL, headers=headers, cookies=cookies, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {HTTP_URL}: {e}")

    assert response.status_code == 403, f"Expected status code 403 when header is wrong, got {response.status_code}"

def test_http_service_missing_cookie():
    headers = {"X-Backdoor-Auth": "falcon99"}

    try:
        response = requests.get(HTTP_URL, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service at {HTTP_URL}: {e}")

    assert response.status_code == 403, f"Expected status code 403 when cookie is missing, got {response.status_code}"

def test_tcp_service():
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=2) as s:
            s.sendall(b"PING\n")
            data = s.recv(1024)
            assert data == b"PONG\n", f"Expected to receive 'PONG\\n', got {data!r}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to TCP service at {TCP_HOST}:{TCP_PORT}")
    except socket.timeout:
        pytest.fail("TCP service timed out waiting for response")
    except Exception as e:
        pytest.fail(f"TCP service failed with error: {e}")