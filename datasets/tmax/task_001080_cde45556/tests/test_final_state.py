# test_final_state.py

import os
import sqlite3
import requests
import pytest

DB_PATH = "/home/user/graph.db"
API_URL = "http://127.0.0.1:8080/shortest_path"
AUTH_HEADER = {"Authorization": "Bearer RESEARCH_TOKEN_99"}

def test_database_exists():
    """Test that the SQLite database was created at the expected location."""
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file"

    # Check if it's a valid SQLite database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        assert len(tables) > 0, "Database exists but contains no tables"
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to SQLite database: {e}")

def test_api_missing_auth():
    """Test that the API returns 401 when the Authorization header is missing."""
    try:
        response = requests.post(API_URL, json={"start": "A", "end": "E"}, timeout=5)
        assert response.status_code == 401, f"Expected status code 401 for missing auth, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_invalid_auth():
    """Test that the API returns 401 when the Authorization header is invalid."""
    try:
        headers = {"Authorization": "Bearer WRONG_TOKEN"}
        response = requests.post(API_URL, json={"start": "A", "end": "E"}, headers=headers, timeout=5)
        assert response.status_code == 401, f"Expected status code 401 for invalid auth, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_shortest_path_a_e():
    """Test the shortest path from A to E."""
    try:
        payload = {"start": "A", "end": "E"}
        response = requests.post(API_URL, json=payload, headers=AUTH_HEADER, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert "path" in data, "Response JSON missing 'path' key"
        assert "cost" in data, "Response JSON missing 'cost' key"

        assert data["path"] == ["A", "C", "D", "E"], f"Expected path ['A', 'C', 'D', 'E'], got {data['path']}"
        assert data["cost"] == 9, f"Expected cost 9, got {data['cost']}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_shortest_path_b_f():
    """Test the shortest path from B to F."""
    try:
        payload = {"start": "B", "end": "F"}
        response = requests.post(API_URL, json=payload, headers=AUTH_HEADER, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert data["path"] == ["B", "C", "F"], f"Expected path ['B', 'C', 'F'], got {data.get('path')}"
        assert data["cost"] == 12, f"Expected cost 12, got {data.get('cost')}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_path_not_found():
    """Test that the API returns 404 when no path exists."""
    try:
        payload = {"start": "A", "end": "Z"}
        response = requests.post(API_URL, json=payload, headers=AUTH_HEADER, timeout=5)
        assert response.status_code == 404, f"Expected status code 404 for non-existent path, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")