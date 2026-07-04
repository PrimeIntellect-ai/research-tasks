# test_final_state.py
import os
import json
import sqlite3

def test_c_file_exists():
    assert os.path.exists('/home/user/detect_deadlocks.c'), "C source file /home/user/detect_deadlocks.c is missing"

def test_executable_exists():
    assert os.path.exists('/home/user/detect_deadlocks'), "Executable /home/user/detect_deadlocks is missing"
    assert os.access('/home/user/detect_deadlocks', os.X_OK), "File /home/user/detect_deadlocks is not executable"

def test_json_output():
    json_path = '/home/user/deadlocks.json'
    assert os.path.exists(json_path), f"Output file {json_path} is missing"

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"Output file {json_path} is not valid JSON"

    assert "deadlocks" in data, "JSON output is missing 'deadlocks' key"

    deadlocks = data["deadlocks"]
    assert isinstance(deadlocks, list), "'deadlocks' should be a list"

    expected_deadlocks = [
        {"tx1": 2, "tx2": 3},
        {"tx1": 4, "tx2": 5}
    ]

    assert len(deadlocks) == len(expected_deadlocks), f"Expected {len(expected_deadlocks)} deadlocks, found {len(deadlocks)}"

    for expected in expected_deadlocks:
        assert expected in deadlocks, f"Expected deadlock {expected} not found in output"

    # Check sorting
    assert deadlocks == expected_deadlocks, f"Deadlocks are not sorted correctly. Expected: {expected_deadlocks}, Got: {deadlocks}"

def test_database_unmodified():
    db_path = '/home/user/audit_logs.db'
    assert os.path.exists(db_path), "Database /home/user/audit_logs.db was deleted"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    tx_count = cursor.fetchone()[0]
    assert tx_count == 6, "Transactions table was modified (row count changed)"

    cursor.execute("SELECT COUNT(*) FROM lock_requests")
    req_count = cursor.fetchone()[0]
    assert req_count == 14, "Lock requests table was modified (row count changed)"

    conn.close()