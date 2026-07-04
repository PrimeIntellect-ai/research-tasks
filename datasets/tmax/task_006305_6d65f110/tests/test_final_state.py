# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/finance.db'
RESULTS_PATH = '/home/user/audit_results.json'

def get_expected_results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = """
    WITH Deadlocks AS (
        SELECT account_id, event_timestamp
        FROM system_events
        WHERE event_code = 'ERR_DEADLOCK'
    ),
    Suspicious AS (
        SELECT DISTINCT d1.account_id
        FROM Deadlocks d1
        JOIN Deadlocks d2 ON d1.account_id = d2.account_id
        WHERE d1.event_timestamp < d2.event_timestamp
          AND (d2.event_timestamp - d1.event_timestamp) <= 3600
    )
    SELECT s.account_id, 
           COALESCE(SUM(CASE WHEN t.tx_type = 'CREDIT' THEN t.amount ELSE 0 END), 0) -
           COALESCE(SUM(CASE WHEN t.tx_type = 'DEBIT' THEN t.amount ELSE 0 END), 0) as net_volume
    FROM Suspicious s
    LEFT JOIN tx_records t ON s.account_id = t.account_id AND t.status = 'COMPLETED'
    GROUP BY s.account_id
    ORDER BY s.account_id ASC
    """

    c.execute(query)
    results = c.fetchall()
    conn.close()

    return [{"account_id": row[0], "net_volume": round(row[1], 2)} for row in results]

def test_results_file_exists():
    assert os.path.isfile(RESULTS_PATH), f"The expected output file {RESULTS_PATH} is missing."

def test_results_content():
    try:
        with open(RESULTS_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {RESULTS_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be an array of objects."

    expected_data = get_expected_results()

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert "account_id" in actual, f"Record {i} is missing 'account_id'"
        assert "net_volume" in actual, f"Record {i} is missing 'net_volume'"

        assert actual["account_id"] == expected["account_id"], \
            f"Expected account_id {expected['account_id']} at index {i}, but got {actual['account_id']}."

        # Check net_volume with a tolerance for floating point inaccuracies
        assert abs(actual["net_volume"] - expected["net_volume"]) < 0.001, \
            f"Expected net_volume {expected['net_volume']} for account {expected['account_id']}, but got {actual['net_volume']}."