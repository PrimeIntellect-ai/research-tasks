# test_final_state.py
import os
import sqlite3
import requests
import pytest

def test_database_deduplicated():
    db_path = "/app/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT src, dst, COUNT(*) FROM edges GROUP BY src, dst HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    conn.close()

    assert len(duplicates) == 0, f"The edges table still contains duplicate records: {duplicates}"

def test_analyze_endpoint_node_1():
    url = "http://127.0.0.1:9000/analyze"
    payload = {"node_id": 1}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    expected_results = [
        {"id": 5, "in_degree": 3},
        {"id": 4, "in_degree": 1},
        {"id": 6, "in_degree": 1}
    ]

    assert "results" in data, "Response JSON is missing the 'results' key."
    assert data["results"] == expected_results, f"Expected results {expected_results}, but got {data['results']}"