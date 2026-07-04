# test_final_state.py
import os
import json
import sqlite3

def test_audit_script_exists():
    path = '/home/user/audit.py'
    assert os.path.exists(path), f"Script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_index_created():
    db_path = '/home/user/access_logs.db'
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='user_access' AND name NOT LIKE 'sqlite_autoindex%'")
    indexes = c.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom index was created on the 'user_access' table to optimize the query."

def test_query_plan_output():
    path = '/home/user/query_plan.txt'
    assert os.path.exists(path), f"Query plan output {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip().upper()

    assert content, f"File {path} is empty."
    assert "USING INDEX" in content, f"Query plan does not indicate the use of an index. Content: {content}"

def test_failed_logins_json():
    json_path = '/home/user/failed_logins.json'
    assert os.path.exists(json_path), f"Output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert isinstance(data, list), f"JSON root must be an array, got {type(data).__name__}."
    assert len(data) == 10, f"Expected exactly 10 records, found {len(data)}."

    # Verify against the actual database truth
    db_path = '/home/user/access_logs.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM user_access WHERE status='failed' ORDER BY timestamp DESC LIMIT 10")
    expected_rows = [dict(row) for row in c.fetchall()]
    conn.close()

    assert len(expected_rows) == 10, "Database does not have enough failed records to verify against."

    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        expected_keys = {'id', 'username', 'ip_address', 'timestamp', 'status'}
        assert set(item.keys()) == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {set(item.keys())}."

        # Check values
        assert item['status'] == 'failed', f"Item at index {i} does not have status 'failed'."

        # Check descending order explicitly
        if i > 0:
            assert data[i-1]['timestamp'] >= data[i]['timestamp'], f"Timestamps are not strictly in descending order at index {i}."

        # Check exact match with database
        assert item == expected_rows[i], f"Item at index {i} does not match the expected database row."