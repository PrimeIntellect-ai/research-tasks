# test_final_state.py

import requests

BASE_URL = "http://127.0.0.1:5050/highest-confidence-frame"
AUTH_HEADER = {"Authorization": "Bearer super-analyst-2024"}

def test_auth_missing():
    try:
        resp = requests.get(f"{BASE_URL}?category=truck", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server: {e}"
    assert resp.status_code == 401, f"Expected 401 Unauthorized when missing auth, got {resp.status_code}"

def test_auth_invalid():
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        resp = requests.get(f"{BASE_URL}?category=truck", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server: {e}"
    assert resp.status_code == 401, f"Expected 401 Unauthorized when invalid auth, got {resp.status_code}"

def test_valid_request_truck():
    try:
        resp = requests.get(f"{BASE_URL}?category=truck", headers=AUTH_HEADER, timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server: {e}"

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Content: {resp.text[:100]}"
    assert resp.headers.get("Content-Type") == "image/jpeg", f"Expected Content-Type image/jpeg, got {resp.headers.get('Content-Type')}"
    assert resp.headers.get("X-Event-Timestamp") == "5.1", f"Expected X-Event-Timestamp 5.1, got {resp.headers.get('X-Event-Timestamp')}"
    assert resp.content.startswith(b"\xff\xd8"), "Response body does not start with JPEG magic bytes (FF D8)"

def test_valid_request_bicycle():
    try:
        resp = requests.get(f"{BASE_URL}?category=bicycle", headers=AUTH_HEADER, timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server: {e}"

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Content: {resp.text[:100]}"
    assert resp.headers.get("Content-Type") == "image/jpeg", f"Expected Content-Type image/jpeg, got {resp.headers.get('Content-Type')}"
    # The bicycle category has highest confidence at event 3, which is 8.0 seconds
    assert resp.headers.get("X-Event-Timestamp") == "8.0", f"Expected X-Event-Timestamp 8.0, got {resp.headers.get('X-Event-Timestamp')}"
    assert resp.content.startswith(b"\xff\xd8"), "Response body does not start with JPEG magic bytes (FF D8)"