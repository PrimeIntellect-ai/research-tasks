# test_final_state.py
import requests
import socket
import pytest
import time

BASE_URL = "http://127.0.0.1:8080"

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Expected JSON response, got: {response.text}")
        assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health: {e}")

def test_score_endpoint_auth_missing():
    try:
        response = requests.post(f"{BASE_URL}/score", json={"crash_count": 7}, timeout=2)
        if response.status_code == 200:
            try:
                data = response.json()
                assert "final_score" not in data, "Server returned final_score without auth header (should be rejected)"
            except ValueError:
                pass
    except requests.exceptions.RequestException:
        # Dropped connection or timeout is acceptable for rejected requests
        pass

def test_score_endpoint_success():
    headers = {"Authorization": "Bearer mobile_ci_secret"}
    try:
        response = requests.post(f"{BASE_URL}/score", json={"crash_count": 7}, headers=headers, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Expected JSON response, got: {response.text}")
        assert data.get("final_score") == 1540, f"Expected {{'final_score': 1540}}, got {data}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /score: {e}")

def test_large_request_no_crash():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", 8080))
        long_url = "/" + "A" * 2000
        request = f"GET {long_url} HTTP/1.1\r\nHost: 127.0.0.1:8080\r\n\r\n"
        s.sendall(request.encode('utf-8'))
        s.recv(1024)
        s.close()
    except Exception:
        # Connection resets or timeouts are fine, as long as the server process doesn't crash
        pass

    time.sleep(0.5)

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        assert response.status_code == 200, "Server returned non-200 after large request"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server crashed or became unresponsive after receiving a large request: {e}")