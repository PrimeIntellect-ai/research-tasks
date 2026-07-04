# test_final_state.py

import os
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"
DB_PATH = "/home/user/app/data.db"

def test_service_is_listening():
    """Ensure the student's HTTP service is up and listening on port 8080."""
    max_retries = 5
    for i in range(max_retries):
        try:
            # Just test if we can connect, even if 404
            requests.get(BASE_URL, timeout=2)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                pytest.fail(f"Could not connect to the service at {BASE_URL}. Is it running?")
            time.sleep(1)

def test_sync_endpoint():
    """Test that the /sync endpoint processes the WebSocket stream correctly."""
    try:
        response = requests.post(f"{BASE_URL}/sync", timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /sync failed: {e}")

    assert response.status_code == 200, f"Expected status code 200 from /sync, got {response.status_code}. Response: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response from /sync is not valid JSON: {response.text}")

    assert json_data.get("status") == "success", f"Expected {{'status': 'success'}} from /sync, got {json_data}"

def test_database_file_exists():
    """Ensure the SQLite database file was created at the correct path."""
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} exists but is not a file"

def test_query_endpoint():
    """Test that the /query endpoint returns the correctly synchronized data."""
    payload = {"query": "SELECT * FROM users ORDER BY id ASC"}
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /query failed: {e}")

    assert response.status_code == 200, f"Expected status code 200 from /query, got {response.status_code}. Response: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response from /query is not valid JSON: {response.text}")

    assert "results" in json_data, f"Expected key 'results' in /query response, got {json_data}"

    expected_results = [
        {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]

    actual_results = json_data["results"]
    assert actual_results == expected_results, f"Expected results {expected_results}, but got {actual_results}"