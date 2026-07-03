# test_final_state.py
import requests
import pytest

def test_honeypot_malicious_payload():
    """Verify the honeypot correctly handles the extracted malicious SQLi payload."""
    url = "http://127.0.0.1:9999/login"
    payload = {"username": "admin' UNION SELECT null, 'root', null--"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to honeypot at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for malicious payload, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response was not valid JSON")

    expected_data = {"status": "escalated", "role": "root"}
    assert data == expected_data, f"Expected JSON {expected_data}, got {data}"

def test_honeypot_normal_payload():
    """Verify the honeypot rejects normal/unmatched payloads."""
    url = "http://127.0.0.1:9999/login"
    payload = {"username": "admin"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to honeypot at {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 for normal payload, got {response.status_code}"