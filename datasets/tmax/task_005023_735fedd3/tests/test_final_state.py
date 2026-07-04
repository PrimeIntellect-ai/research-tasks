# test_final_state.py

import os
import sqlite3
import requests
import pytest

def test_database_exists_and_indexed():
    """Check that the SQLite database exists, has the correct table, indexes, and data."""
    db_path = "/app/graph.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges'")
    assert cursor.fetchone() is not None, "Table 'edges' does not exist in graph.db."

    # Check for indexes on edges table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on the 'edges' table. Query optimization was not implemented."

    # Check data is populated
    cursor.execute("SELECT COUNT(*) FROM edges")
    count = cursor.fetchone()[0]
    assert count >= 5, f"The edges table only contains {count} rows. Expected at least 5 rows from the extracted subtitle data."

    conn.close()

def test_http_api_unauthorized():
    """Check that the API rejects requests without the correct authorization header."""
    url = "http://127.0.0.1:8080/api/two-hop?start=A&end=D"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service on port 8080: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing auth header, got {response.status_code}."

def test_http_api_authorized_and_correct_logic():
    """Check that the API returns the correct 2-hop paths, correctly joining the graph and ordered by weight."""
    url = "http://127.0.0.1:8080/api/two-hop?start=A&end=D"
    headers = {"Authorization": "Bearer graph-admin-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected = [
        {"path": "A->C->D", "total_weight": 11},
        {"path": "A->B->D", "total_weight": 15}
    ]

    assert data == expected, f"API returned incorrect data.\nExpected: {expected}\nGot: {data}"