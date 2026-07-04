# test_final_state.py

import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_server():
    """Wait for the server to be up and running."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            # Just check if the port is open by attempting a connection
            requests.get(BASE_URL, timeout=1)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
        except requests.exceptions.Timeout:
            pass
    pytest.fail("Server is not listening on 127.0.0.1:8080")

@pytest.fixture(scope="module", autouse=True)
def setup():
    wait_for_server()

def test_valid_login_test():
    url = f"{BASE_URL}/login"
    data = {"token": "46554746", "redirect": "/home"}

    try:
        response = requests.post(url, data=data, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to connect or send request: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    csp_header = response.headers.get("Content-Security-Policy", "")
    assert "default-src 'self';" in csp_header, f"Missing or incorrect CSP header. Got: {csp_header}"

    assert response.text.strip() == "test", f"Expected body 'test', got '{response.text}'"

def test_invalid_redirect_http():
    url = f"{BASE_URL}/login"
    data = {"token": "46554746", "redirect": "http://evil.com"}

    try:
        response = requests.post(url, data=data, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to connect or send request: {e}")

    assert response.status_code == 400, f"Expected status 400 for absolute redirect, got {response.status_code}. Response: {response.text}"

def test_invalid_redirect_protocol_relative():
    url = f"{BASE_URL}/login"
    data = {"token": "445b5b46", "redirect": "//attacker.com"}

    try:
        response = requests.post(url, data=data, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to connect or send request: {e}")

    assert response.status_code == 400, f"Expected status 400 for protocol-relative redirect, got {response.status_code}. Response: {response.text}"

def test_valid_login_root():
    url = f"{BASE_URL}/login"
    data = {"token": "445b5b46", "redirect": "/settings"}

    try:
        response = requests.post(url, data=data, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to connect or send request: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    csp_header = response.headers.get("Content-Security-Policy", "")
    assert "default-src 'self';" in csp_header, f"Missing or incorrect CSP header. Got: {csp_header}"

    assert response.text.strip() == "root", f"Expected body 'root', got '{response.text}'"