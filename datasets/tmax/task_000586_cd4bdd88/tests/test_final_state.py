# test_final_state.py
import os
import sqlite3
import requests
import pytest

DB_PATH = "/home/user/audit.db"
BASE_URL = "http://127.0.0.1:9090"
HEADERS = {"X-Compliance-Key": "alpha-audit-99"}

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    # Check if transactions table exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "Table 'transactions' does not exist in the database."

def test_api_unauthorized():
    # Test GET without header
    try:
        response = requests.get(f"{BASE_URL}/api/cycles")
    except requests.exceptions.ConnectionError:
        pytest.fail("API service is not running or not reachable at 127.0.0.1:9090")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for unauthorized request, got {response.status_code}"

def test_api_cycles():
    try:
        response = requests.get(f"{BASE_URL}/api/cycles", headers=HEADERS)
    except requests.exceptions.ConnectionError:
        pytest.fail("API service is not running or not reachable at 127.0.0.1:9090")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Response should be a JSON array"
    assert len(data) >= 1, "Expected at least one cycle in the response"

    # Check if ["U101", "U102", "U103"] is in the response
    expected_cycle = ["U101", "U102", "U103"]
    assert expected_cycle in data, f"Expected cycle {expected_cycle} not found in response: {data}"

def test_api_deadlock():
    try:
        response = requests.post(f"{BASE_URL}/api/deadlock", headers=HEADERS)
    except requests.exceptions.ConnectionError:
        pytest.fail("API service is not running or not reachable at 127.0.0.1:9090")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert data.get("status") == "deadlocked", f"Expected status 'deadlocked', got {data.get('status')}"