# test_final_state.py

import os
import sqlite3
import requests
import pytest

def test_database_indices_and_integrity():
    db_path = "/home/user/metadata.db"
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check database integrity (this will fail if idx_parent is still corrupted)
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    assert result is not None and result[0].lower() == "ok", f"Database integrity check failed: {result}"

    # Check for the new index idx_opt
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_opt';")
    assert cursor.fetchone() is not None, "Index 'idx_opt' was not created."

    # Check columns of idx_opt
    cursor.execute("PRAGMA index_info(idx_opt);")
    columns = [row[2] for row in cursor.fetchall()]
    expected_columns = ["id", "parent_id", "size", "backup_time"]
    assert columns == expected_columns, f"Index 'idx_opt' has incorrect columns. Expected {expected_columns}, got {columns}"

    conn.close()

def test_http_service_response():
    url = "http://127.0.0.1:8080/chain?id=5"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the backup service at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Expected a JSON array, got {type(data).__name__}"
    assert len(data) > 0, "Expected a non-empty JSON array representing the backup chain."

    # Verify the structure and values of the response
    expected_keys = {"id", "parent_id", "size", "cumulative_size"}
    for item in data:
        missing_keys = expected_keys - set(item.keys())
        assert not missing_keys, f"JSON object missing expected keys {missing_keys}: {item}"

    # The last element should be the requested node (id=5)
    assert data[-1]["id"] == 5, f"Expected the last node in the chain to have id=5, got {data[-1]['id']}"

    # Verify cumulative size logic
    expected_cumulative = 0
    for item in data:
        expected_cumulative += item["size"]
        assert item["cumulative_size"] == expected_cumulative, \
            f"Cumulative size mismatch for node {item['id']}. Expected {expected_cumulative}, got {item['cumulative_size']}"