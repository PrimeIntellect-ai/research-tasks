# test_final_state.py

import time
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
TOKEN_HEADER = {"Authorization": "Bearer AUDITOR-TOKEN-992"}

@pytest.fixture(scope="module", autouse=True)
def wait_for_server():
    """Wait for the server to become available before running tests."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            requests.get(f"{BASE_URL}/receipt", timeout=1)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    pytest.fail("Server did not start on 127.0.0.1:8080")

def test_auth_required():
    """Test that requests without the correct token return 401."""
    response = requests.get(f"{BASE_URL}/receipt")
    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_get_receipt_with_token():
    """Test GET /receipt with valid token."""
    response = requests.get(f"{BASE_URL}/receipt", headers=TOKEN_HEADER)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.headers.get("Content-Security-Policy") == "default-src 'self'", "Missing or incorrect Content-Security-Policy header"

    text = response.text
    assert "XXXX-XXXX-XXXX-XXXX" in text, "Expected redacted credit card in response"
    assert "4128-9999-1234-5678" not in text, "Expected original credit card to be redacted"

def test_post_redact_valid():
    """Test POST /redact with valid text."""
    payload = "My card is 1111-2222-3333-4444!"
    response = requests.post(f"{BASE_URL}/redact", headers=TOKEN_HEADER, data=payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.headers.get("Content-Security-Policy") == "default-src 'self'", "Missing or incorrect Content-Security-Policy header"
    assert response.text == "My card is XXXX-XXXX-XXXX-XXXX!", f"Unexpected redacted text: {response.text}"

def test_post_redact_waf_script():
    """Test POST /redact with <script> payload triggers WAF."""
    payload = "<script>alert(1)</script>"
    response = requests.post(f"{BASE_URL}/redact", headers=TOKEN_HEADER, data=payload)
    assert response.status_code == 403, f"Expected 403 Forbidden for <script> payload, got {response.status_code}"

def test_post_redact_waf_sql():
    """Test POST /redact with UNION SELECT payload triggers WAF."""
    payload = "id=1 UNION SELECT password FROM users"
    response = requests.post(f"{BASE_URL}/redact", headers=TOKEN_HEADER, data=payload)
    assert response.status_code == 403, f"Expected 403 Forbidden for UNION SELECT payload, got {response.status_code}"