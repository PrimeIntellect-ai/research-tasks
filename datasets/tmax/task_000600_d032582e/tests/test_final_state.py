# test_final_state.py
import os
import requests
import pytest

API_BASE_URL = "http://127.0.0.1:9090"

def test_sqlite_db_exists():
    """Verify that the SQLite database was created at the expected location."""
    db_path = "/home/user/locks.db"
    assert os.path.isfile(db_path), f"SQLite database not found at {db_path}"

def test_deadlock_endpoint():
    """Verify the /api/deadlock endpoint returns the correct cycle."""
    url = f"{API_BASE_URL}/api/deadlock"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    result = response.text.strip()
    expected = "Tx101,Tx102,Tx103"
    assert result == expected, f"Expected deadlock response '{expected}', but got '{result}'"

def test_blocker_endpoint():
    """Verify the /api/blocker endpoint returns the transaction with the highest blocker centrality."""
    url = f"{API_BASE_URL}/api/blocker"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    result = response.text.strip()
    expected = "Tx103"
    assert result == expected, f"Expected blocker response '{expected}', but got '{result}'"