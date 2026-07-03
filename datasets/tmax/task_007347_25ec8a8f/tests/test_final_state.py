# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_events_db_populated():
    db_path = "/home/user/events.db"
    assert os.path.isfile(db_path), f"Expected database {db_path} to exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    assert cursor.fetchone() is not None, "Table 'events' does not exist in the database."

    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    assert count == 6, f"Expected 6 records in the 'events' table, but found {count}."

    conn.close()

def test_aggregate_go_exists():
    path = "/home/user/aggregate.go"
    assert os.path.isfile(path), f"Expected file {path} to exist."

def test_output_json_correct():
    path = "/home/user/output.json"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert isinstance(data, list), "Expected output.json to contain a JSON array."
    assert len(data) == 4, f"Expected 4 aggregated records, but found {len(data)}."

    expected_totals = {
        101: 20,
        104: 20,
        102: 18,
        103: 2
    }

    for item in data:
        assert "user_id" in item, "Missing 'user_id' in JSON object."
        assert "total_duration" in item, "Missing 'total_duration' in JSON object."
        user_id = item["user_id"]
        total_duration = item["total_duration"]
        assert user_id in expected_totals, f"Unexpected user_id {user_id} in output."
        assert expected_totals[user_id] == total_duration, f"Expected total_duration {expected_totals[user_id]} for user_id {user_id}, but got {total_duration}."

    # Check sorting (descending by total_duration)
    durations = [item["total_duration"] for item in data]
    assert durations == sorted(durations, reverse=True), "Expected output to be sorted by total_duration in descending order."

def test_index_created():
    db_path = "/home/user/events.db"
    assert os.path.isfile(db_path), f"Expected database {db_path} to exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='events'")
    indices = cursor.fetchall()
    assert len(indices) > 0, "Expected an index to be created on the 'events' table."

    conn.close()

def test_plan_txt_exists_and_valid():
    path = "/home/user/plan.txt"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        content = f.read().upper()

    assert "EVENTS" in content, "Expected the query plan to reference the 'events' table."
    assert "SCAN" in content or "SEARCH" in content, "Expected the query plan to contain 'SCAN' or 'SEARCH'."