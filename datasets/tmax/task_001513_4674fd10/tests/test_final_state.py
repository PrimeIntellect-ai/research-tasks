# test_final_state.py

import os
import json
import sqlite3
import pytest
import requests

def test_libjsonparse_compiled():
    """Verify that libjsonparse.a has been successfully compiled."""
    lib_path = "/app/vendored/libjsonparse-1.2/libjsonparse.a"
    assert os.path.isfile(lib_path), f"Library {lib_path} was not compiled."

def test_http_service_and_db_export():
    """
    Test the full workflow of the HTTP service:
    1. Ingest JSONL data with unicode escapes.
    2. Check rolling stats.
    3. Export to SQLite database.
    4. Verify SQLite database contents.
    """
    base_url = "http://127.0.0.1:8080"

    # 1. Ingest data
    payload = (
        '{"timestamp": 1, "value": 10.0, "event_name": "test1"}\n'
        '{"timestamp": 2, "value": 20.0, "event_name": "test\\u00e9"}\n'
        '{"timestamp": 3, "value": 30.0, "event_name": "test\\u00f1"}\n'
    )

    try:
        response_ingest = requests.post(f"{base_url}/ingest", data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to or send data to POST /ingest: {e}")

    assert response_ingest.status_code in (200, 201, 202, 204), \
        f"Expected successful status code for POST /ingest, got {response_ingest.status_code}"

    # 2. Check rolling stats
    try:
        response_stats = requests.get(f"{base_url}/rolling_stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /rolling_stats: {e}")

    assert response_stats.status_code == 200, \
        f"Expected HTTP 200 for GET /rolling_stats, got {response_stats.status_code}"

    try:
        stats_data = response_stats.json()
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON from GET /rolling_stats. Response body: {response_stats.text}")

    assert "rolling_avg" in stats_data, "Response JSON missing 'rolling_avg' key."
    assert float(stats_data["rolling_avg"]) == 20.0, \
        f"Expected rolling_avg to be 20.0, got {stats_data['rolling_avg']}"

    # 3. Export to database
    try:
        response_export = requests.post(f"{base_url}/export", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /export: {e}")

    assert response_export.status_code == 200, \
        f"Expected HTTP 200 for POST /export, got {response_export.status_code}"

    # 4. Verify SQLite database
    db_path = "/home/user/analytics.db"
    assert os.path.isfile(db_path), f"Database file {db_path} was not created."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM events WHERE event_name LIKE '%é%' OR event_name LIKE '%ñ%';")
        count = cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'events' table in {db_path}: {e}")
    finally:
        conn.close()

    assert count >= 2, f"Expected at least 2 events with unicode characters in the database, found {count}."