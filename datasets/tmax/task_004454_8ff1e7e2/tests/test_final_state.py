# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:9000"
TOKEN = "TR4CK_M3_N0W"

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

def test_server_health():
    assert wait_for_server(f"{BASE_URL}/health"), "Server is not reachable on 127.0.0.1:9000. Did you start the server in the background?"

    response = requests.get(f"{BASE_URL}/health", timeout=2)
    assert response.status_code == 200, f"Expected status 200 for /health, got {response.status_code}"

def test_server_set_and_get():
    # Ensure server is up before testing
    assert wait_for_server(f"{BASE_URL}/health"), "Server is not reachable on 127.0.0.1:9000."

    headers = {"Authorization": f"Bearer {TOKEN}"}

    # Test POST /set
    post_url = f"{BASE_URL}/set?key=test&val=123"
    post_resp = requests.post(post_url, headers=headers, timeout=2)
    assert post_resp.status_code == 200, f"Expected status 200 for POST /set, got {post_resp.status_code}. Response: {post_resp.text}"

    # Test GET /get
    get_url = f"{BASE_URL}/get?key=test"
    get_resp = requests.get(get_url, headers=headers, timeout=2)
    assert get_resp.status_code == 200, f"Expected status 200 for GET /get, got {get_resp.status_code}. Response: {get_resp.text}"
    assert get_resp.text.strip() == "123", f"Expected body '123', got '{get_resp.text}'"