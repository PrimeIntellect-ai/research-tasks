# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_service():
    """Wait for the student's API to become available."""
    for _ in range(10):
        try:
            # Just test if the port is open and responding to HTTP
            requests.get(f"{BASE_URL}/", timeout=1)
            return
        except requests.exceptions.RequestException:
            time.sleep(1)

@pytest.fixture(autouse=True, scope="session")
def setup():
    wait_for_service()

def test_shortest_path_e2_e3():
    """Test shortest path from E2 to E3."""
    response = requests.get(f"{BASE_URL}/shortest_path", params={"src_entity": "E2", "dst_entity": "E3"}, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "path" in data, f"Missing 'path' key in response: {data}"

    expected_path = ["E2", "A3", "A4", "E3"]
    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"

def test_shortest_path_e2_e4():
    """Test shortest path from E2 to E4."""
    response = requests.get(f"{BASE_URL}/shortest_path", params={"src_entity": "E2", "dst_entity": "E4"}, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "path" in data, f"Missing 'path' key in response: {data}"

    expected_path = ["E2", "A3", "A1", "A5", "E4"]
    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"

def test_exposure_e1_full():
    """Test exposure for E1 with limit=10, offset=0."""
    response = requests.get(f"{BASE_URL}/exposure", params={"entity_id": "E1", "limit": 10, "offset": 0}, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "accounts" in data, f"Missing 'accounts' key in response: {data}"

    expected_accounts = ["A5", "A3"]
    assert data["accounts"] == expected_accounts, f"Expected accounts {expected_accounts}, got {data['accounts']}"

def test_exposure_e1_pagination():
    """Test exposure for E1 with limit=1, offset=1."""
    response = requests.get(f"{BASE_URL}/exposure", params={"entity_id": "E1", "limit": 1, "offset": 1}, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "accounts" in data, f"Missing 'accounts' key in response: {data}"

    expected_accounts = ["A3"]
    assert data["accounts"] == expected_accounts, f"Expected accounts {expected_accounts}, got {data['accounts']}"