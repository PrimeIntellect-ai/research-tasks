# test_final_state.py
import time
import requests

BASE_URL = "http://127.0.0.1:8080"

def wait_for_server():
    """Wait up to 5 seconds for the server to be available."""
    for _ in range(10):
        try:
            requests.get(f"{BASE_URL}/status", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_server_status():
    assert wait_for_server(), "Server is not listening on 127.0.0.1:8080 or did not respond in time"

    resp = requests.get(f"{BASE_URL}/status", timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK for /status, got {resp.status_code}"

    data = resp.json()
    assert data.get("status") == "ready", f"Expected {{'status': 'ready'}}, got {data}"

def test_curate_unauthorized():
    assert wait_for_server(), "Server is not listening on 127.0.0.1:8080"

    resp = requests.post(f"{BASE_URL}/curate", timeout=2)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for /curate without auth, got {resp.status_code}"

def test_curate_authorized():
    assert wait_for_server(), "Server is not listening on 127.0.0.1:8080"

    headers = {"Authorization": "Bearer delta charlie seven"}
    resp = requests.post(f"{BASE_URL}/curate", headers=headers, timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK for /curate with valid auth, got {resp.status_code}"

    data = resp.json()
    assert "valid_files" in data, f"Response missing 'valid_files' key: {data}"

    valid_files = data["valid_files"]
    assert isinstance(valid_files, list), "'valid_files' should be a list"

    expected_files = {"/readme.txt", "/data/info.json"}
    actual_files = set(valid_files)

    assert actual_files == expected_files, f"Expected valid_files to be {expected_files}, but got {actual_files}"