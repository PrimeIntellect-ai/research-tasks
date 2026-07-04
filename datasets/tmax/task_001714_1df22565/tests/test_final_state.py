# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_top_users_output():
    json_path = '/home/user/top_users.json'
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    db_path = '/home/user/communications.db'
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Recompute the expected top users directly from the database
    query = """
    SELECT u.handle, 
           (SELECT COUNT(*) FROM event_links WHERE source_uid = u.uid OR target_uid = u.uid) as score
    FROM system_users u
    WHERE (SELECT COUNT(*) FROM event_links WHERE source_uid = u.uid OR target_uid = u.uid) > 2
    ORDER BY score DESC, u.handle ASC
    LIMIT 3
    """

    try:
        cur.execute(query)
        expected_rows = cur.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query database {db_path}: {e}")
    finally:
        conn.close()

    expected_data = [
        {"username": row[0], "communication_score": row[1]}
        for row in expected_rows
    ]

    assert isinstance(actual_data, list), f"Expected JSON root to be a list, but got {type(actual_data).__name__}"
    assert actual_data == expected_data, f"Data in {json_path} does not match the expected output. Expected: {expected_data}, Actual: {actual_data}"