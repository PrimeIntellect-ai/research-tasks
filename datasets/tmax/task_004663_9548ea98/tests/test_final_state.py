# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/compliance.db'
INDEX_SQL_PATH = '/home/user/index.sql'
CPP_PATH = '/home/user/audit.cpp'
RUNNER_PATH = '/home/user/audit_runner'
RESULTS_PATH = '/home/user/audit_results.json'

def test_index_sql_exists_and_valid():
    assert os.path.exists(INDEX_SQL_PATH), f"Missing index script at {INDEX_SQL_PATH}"
    with open(INDEX_SQL_PATH, 'r') as f:
        content = f.read().lower()

    assert "create index" in content, "index.sql must contain a CREATE INDEX statement."
    assert "access_logs" in content, "index.sql must target the access_logs table."
    assert "user_id" in content, "index.sql must index the user_id column."

def test_cpp_file_exists():
    assert os.path.exists(CPP_PATH), f"Missing C++ source file at {CPP_PATH}"

def test_runner_executable_exists():
    assert os.path.exists(RUNNER_PATH), f"Missing compiled executable at {RUNNER_PATH}"
    assert os.access(RUNNER_PATH, os.X_OK), f"{RUNNER_PATH} is not executable."

def get_expected_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT 
        t.tx_id, 
        t.user_id, 
        t.amount, 
        a.ip_address as flagged_ip
    FROM transactions t
    JOIN users u ON t.user_id = u.user_id
    JOIN access_logs a ON t.user_id = a.user_id
    WHERE t.amount > 10000
      AND a.ip_country != u.country_code
      AND abs(julianday(a.log_timestamp) - julianday(t.tx_timestamp)) <= 1.0
    ORDER BY a.log_timestamp DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # In case of multiple logs for a transaction, we need the most recent one.
    # We can group by tx_id and pick the first one since we ordered by log_timestamp DESC.
    results_map = {}
    for row in rows:
        tx_id, user_id, amount, flagged_ip = row
        if tx_id not in results_map:
            results_map[tx_id] = {
                "tx_id": tx_id,
                "user_id": user_id,
                "amount": float(amount),
                "flagged_ip": flagged_ip
            }

    return list(results_map.values())

def test_audit_results_json():
    assert os.path.exists(RESULTS_PATH), f"Missing results file at {RESULTS_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_PATH} does not contain valid JSON.")

    assert isinstance(actual_results, list), "JSON output must be a list of objects."

    expected_results = get_expected_results()

    # Sort both lists by tx_id to ensure order-independent comparison
    actual_sorted = sorted(actual_results, key=lambda x: x.get("tx_id", ""))
    expected_sorted = sorted(expected_results, key=lambda x: x["tx_id"])

    assert len(actual_sorted) == len(expected_sorted), \
        f"Expected {len(expected_sorted)} results, got {len(actual_sorted)}."

    for actual, expected in zip(actual_sorted, expected_sorted):
        assert actual.get("tx_id") == expected["tx_id"], "Mismatch in tx_id."
        assert actual.get("user_id") == expected["user_id"], "Mismatch in user_id."
        assert abs(actual.get("amount", 0) - expected["amount"]) < 0.01, "Mismatch in amount."
        assert actual.get("flagged_ip") == expected["flagged_ip"], "Mismatch in flagged_ip."