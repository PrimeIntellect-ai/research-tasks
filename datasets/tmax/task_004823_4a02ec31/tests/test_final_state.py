# test_final_state.py
import pytest
import requests
import sqlite3
import os

BASE_URL = "http://127.0.0.1:9090/api/v1/route-to-root"
PASSPHRASE = "epsilon protocol active"
HEADERS = {"Authorization": f"Bearer {PASSPHRASE}"}

def test_service_unauthorized():
    """Test that the service rejects unauthorized requests."""
    try:
        response = requests.post(
            BASE_URL,
            headers={"Authorization": "Bearer wrong token"},
            json={"target_node": 5},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {BASE_URL}. Is it running? Error: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for bad token, got {response.status_code}"

def test_service_missing_auth():
    """Test that the service rejects requests with no auth header."""
    try:
        response = requests.post(
            BASE_URL,
            json={"target_node": 5},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {BASE_URL}. Is it running? Error: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

def test_service_valid_route():
    """Test that the service returns the correct route for a valid node."""
    try:
        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            json={"target_node": 5},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {BASE_URL}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "path" in data, f"Response JSON missing 'path' key: {data}"

    # Calculate the expected path dynamically from the DB to be robust
    db_path = '/app/routing.sqlite'
    assert os.path.isfile(db_path), "Database file missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    expected_path = []
    current_node = 5
    while current_node is not None:
        expected_path.append(current_node)
        cursor.execute("SELECT parent_id FROM network_topology WHERE id = ?", (current_node,))
        row = cursor.fetchone()
        if not row:
            break
        current_node = row[0]

    conn.close()

    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"

def test_service_not_found():
    """Test that the service returns 404 for a non-existent node."""
    try:
        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            json={"target_node": 999999},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {BASE_URL}. Is it running? Error: {e}")

    assert response.status_code == 404, f"Expected 404 Not Found for non-existent node, got {response.status_code}"