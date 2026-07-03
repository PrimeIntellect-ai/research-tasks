# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/network.db"
JSON_PATH = "/home/user/top_influencers.json"

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

def test_interaction_graph_table():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='interaction_graph'")
    assert cursor.fetchone() is not None, "Table 'interaction_graph' does not exist."

    # Check columns
    cursor.execute("PRAGMA table_info(interaction_graph)")
    columns = {row[1] for row in cursor.fetchall()}
    expected_columns = {"source_email", "target_email", "total_weight"}
    assert expected_columns.issubset(columns), f"Table 'interaction_graph' is missing required columns. Found: {columns}"

    # Check a specific computed weight (e.g., alice to bob code_review = 2 * 5 = 10)
    cursor.execute("SELECT total_weight FROM interaction_graph WHERE source_email='alice@company.com' AND target_email='bob@company.com'")
    row = cursor.fetchone()
    assert row is not None, "Missing edge from alice to bob in interaction_graph."
    assert row[0] == 10, f"Expected total_weight 10 for alice->bob, got {row[0]}"

    # Check grace to alice (code_review = 3 * 5 = 15)
    cursor.execute("SELECT total_weight FROM interaction_graph WHERE source_email='grace@company.com' AND target_email='alice@company.com'")
    row = cursor.fetchone()
    assert row is not None, "Missing edge from grace to alice in interaction_graph."
    assert row[0] == 15, f"Expected total_weight 15 for grace->alice, got {row[0]}"

    conn.close()

def test_indexes_exist():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if any indexes exist on interaction_graph
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='interaction_graph'")
    indexes_graph = cursor.fetchall()
    assert len(indexes_graph) > 0, "No indexes found on 'interaction_graph' table."

    # Check if any indexes exist on the employee table (we don't know the exact name, but likely 'employees')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name IN (SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%employee%')")
    indexes_emp = cursor.fetchall()
    assert len(indexes_emp) > 0, "No indexes found on the employee table."

    conn.close()

def test_json_output():
    assert os.path.isfile(JSON_PATH), f"Output file {JSON_PATH} does not exist."

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON output must be a list of objects."

    expected_data = [
        {"department": "Engineering", "email": "grace@company.com", "incoming_weight": 60, "rank": 1},
        {"department": "Engineering", "email": "bob@company.com", "incoming_weight": 45, "rank": 2},
        {"department": "Marketing", "email": "frank@company.com", "incoming_weight": 20, "rank": 1},
        {"department": "Marketing", "email": "eve@company.com", "incoming_weight": 10, "rank": 2},
        {"department": "Sales", "email": "charlie@company.com", "incoming_weight": 40, "rank": 1},
        {"department": "Sales", "email": "diana@company.com", "incoming_weight": 2, "rank": 2}
    ]

    # Sort both to compare regardless of order
    def sort_key(item):
        return (item.get("department", ""), item.get("rank", 0))

    data_sorted = sorted(data, key=sort_key)
    expected_sorted = sorted(expected_data, key=sort_key)

    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} results, got {len(data_sorted)}."

    for actual, expected in zip(data_sorted, expected_sorted):
        assert actual == expected, f"Mismatch in JSON output.\nExpected: {expected}\nGot: {actual}"