# test_final_state.py
import requests
import pytest

PROXY_URL = "http://127.0.0.1:9000"

def test_proxy_malicious_redirect_and_cookie_security():
    """
    Test Request 1: Valid new login + malicious redirect.
    Verifies credential rotation, open redirect mitigation, and session security upgrades.
    """
    url = f"{PROXY_URL}/login?redirect=http://attacker.com"
    data = {"username": "admin", "password": "SuperSafeRotated99"}

    try:
        # allow_redirects=False is crucial to inspect the 302 response itself
        response = requests.post(url, data=data, allow_redirects=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the proxy on port 9000. Ensure your proxy is running and bound to 0.0.0.0:9000.")
    except requests.exceptions.Timeout:
        pytest.fail("Request to proxy timed out.")

    assert response.status_code == 302, f"Expected status 302 for valid rotated credentials, got {response.status_code}. Response body: {response.text}"

    location = response.headers.get("Location")
    assert location == "/dashboard", f"Open redirect mitigation failed. Expected Location header to be sanitized to '/dashboard', got '{location}'"

    set_cookie = response.headers.get("Set-Cookie")
    assert set_cookie is not None, "Expected a 'Set-Cookie' header in the response, but none was found."

    cookie_lower = set_cookie.lower()
    assert "secure" in cookie_lower, f"'Secure' attribute missing from Set-Cookie header: {set_cookie}"
    assert "httponly" in cookie_lower, f"'HttpOnly' attribute missing from Set-Cookie header: {set_cookie}"
    assert "samesite=strict" in cookie_lower, f"'SameSite=Strict' attribute missing from Set-Cookie header: {set_cookie}"

def test_proxy_safe_redirect():
    """
    Test Request 2: Valid new login + safe redirect.
    Verifies that valid relative redirects are allowed.
    """
    url = f"{PROXY_URL}/login?redirect=/profile"
    data = {"username": "admin", "password": "SuperSafeRotated99"}

    try:
        response = requests.post(url, data=data, allow_redirects=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the proxy on port 9000.")

    assert response.status_code == 302, f"Expected status 302 for valid rotated credentials, got {response.status_code}. Response body: {response.text}"

    location = response.headers.get("Location")
    assert location == "/profile", f"Safe redirect failed. Expected Location header to remain '/profile', got '{location}'"

def test_proxy_rejects_old_credentials():
    """
    Test Request 3: Old credentials.
    Verifies that the old hardcoded credentials cannot be used externally anymore.
    """
    url = f"{PROXY_URL}/login"
    data = {"username": "admin", "password": "v1nt4g3_p4ssw0rd"}

    try:
        response = requests.post(url, data=data, allow_redirects=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the proxy on port 9000.")

    assert response.status_code in (401, 403), f"Expected status 401 or 403 when attempting to login with old credentials, got {response.status_code}. The proxy must not allow the old password from external clients."