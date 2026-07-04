# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/compliance_audit/audit.db"
REPORT_PATH = "/home/user/compliance_audit/report.json"

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

def test_transactions_table_and_indexes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
    table = cursor.fetchone()
    assert table is not None, "Table 'transactions' does not exist in the database."

    # Check if there are any indexes on the transactions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='transactions';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on the 'transactions' table. Indexing strategy is missing."

    conn.close()

def test_report_json_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_report_json_content():
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    assert "audit_threshold" in report, "Missing 'audit_threshold' in report.json"
    assert report["audit_threshold"] == 50000.0, f"Expected audit_threshold 50000.0, got {report['audit_threshold']}"

    assert "cycles_detected" in report, "Missing 'cycles_detected' in report.json"
    cycles = report["cycles_detected"]

    assert isinstance(cycles, list), "'cycles_detected' must be a list."

    # Check schema and values
    expected_cycles = [
        {
            "node1": "U4444",
            "node2": "U5555",
            "node3": "U6666",
            "bottleneck_amount": 80000.0
        },
        {
            "node1": "U1111",
            "node2": "U2222",
            "node3": "U3333",
            "bottleneck_amount": 55000.0
        }
    ]

    assert len(cycles) == len(expected_cycles), f"Expected {len(expected_cycles)} cycles, found {len(cycles)}."

    for i, (actual, expected) in enumerate(zip(cycles, expected_cycles)):
        assert "node1" in actual and "node2" in actual and "node3" in actual and "bottleneck_amount" in actual, \
            f"Cycle at index {i} is missing required keys."

        assert actual["node1"] == expected["node1"], f"Expected node1 '{expected['node1']}' at index {i}, got '{actual['node1']}'"
        assert actual["node2"] == expected["node2"], f"Expected node2 '{expected['node2']}' at index {i}, got '{actual['node2']}'"
        assert actual["node3"] == expected["node3"], f"Expected node3 '{expected['node3']}' at index {i}, got '{actual['node3']}'"
        assert actual["bottleneck_amount"] == expected["bottleneck_amount"], \
            f"Expected bottleneck_amount {expected['bottleneck_amount']} at index {i}, got {actual['bottleneck_amount']}"