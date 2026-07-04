# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = '/home/user/api.db'
DSL_PATH = '/home/user/queries.dsl'
LOG_PATH = '/home/user/test_results.log'

def get_expected_v2_data():
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT id, endpoint, payload_encoded FROM mocks_v1 ORDER BY id")
        rows = c.fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    expected = []
    for row in rows:
        row_id, endpoint, payload_encoded = row
        decoded = bytes.fromhex(payload_encoded).decode('utf-16le')
        # format: status=<integer>,body=<string>
        parts = decoded.split(',', 1)
        status = int(parts[0].split('=')[1])
        body = parts[1].split('=', 1)[1]
        expected.append((row_id, endpoint, status, body))
    return expected

def test_mocks_v2_table():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mocks_v2'")
    assert c.fetchone() is not None, "Table 'mocks_v2' does not exist in the database."

    c.execute("PRAGMA table_info(mocks_v2)")
    columns = {row[1]: row[2].upper() for row in c.fetchall()}

    assert 'id' in columns, "Column 'id' is missing from 'mocks_v2'."
    assert 'endpoint' in columns, "Column 'endpoint' is missing from 'mocks_v2'."
    assert 'status_code' in columns, "Column 'status_code' is missing from 'mocks_v2'."
    assert 'response_body' in columns, "Column 'response_body' is missing from 'mocks_v2'."

    c.execute("SELECT id, endpoint, status_code, response_body FROM mocks_v2 ORDER BY id")
    actual_rows = c.fetchall()
    conn.close()

    expected_rows = get_expected_v2_data()
    assert expected_rows, "Could not compute expected data (mocks_v1 might be missing or corrupted)."

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in 'mocks_v2', got {len(actual_rows)}."
    assert actual_rows == expected_rows, "Data in 'mocks_v2' does not match the expected decoded values."

def test_results_log():
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} is missing."
    assert os.path.exists(DSL_PATH), f"DSL file {DSL_PATH} is missing."

    expected_v2_data = get_expected_v2_data()
    db_map = {row[1]: (row[2], row[3]) for row in expected_v2_data}

    with open(DSL_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_log = []
    for i in range(0, len(lines), 2):
        if not lines[i].startswith("EXEC "): 
            continue
        endpoint = lines[i].split(" ", 1)[1]
        assert_status = int(lines[i+1].split(" ")[1])

        if endpoint not in db_map:
            expected_log.append(f"[{endpoint}] ERROR: not found\n")
        else:
            db_status, db_body = db_map[endpoint]
            if db_status == assert_status:
                expected_log.append(f"[{endpoint}] PASS: {db_body}\n")
            else:
                expected_log.append(f"[{endpoint}] FAIL: expected {assert_status}, got {db_status}\n")

    with open(LOG_PATH, 'r') as f:
        actual_log = f.readlines()

    assert len(actual_log) == len(expected_log), f"Expected {len(expected_log)} lines in {LOG_PATH}, got {len(actual_log)}."

    for i, (actual, expected) in enumerate(zip(actual_log, expected_log)):
        assert actual == expected, f"Mismatch at line {i+1} in {LOG_PATH}.\nExpected: {expected.strip()}\nGot: {actual.strip()}"