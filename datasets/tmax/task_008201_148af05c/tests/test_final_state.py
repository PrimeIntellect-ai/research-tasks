# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/store.db"
PLAN_PATH = "/home/user/plan.txt"
JSON_PATH = "/home/user/top_pending.json"

def test_index_exists_and_correct():
    """Verify that the composite index was created on the correct table and columns."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if index exists
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name='idx_orders_status_date';")
    index_info = cursor.fetchone()
    assert index_info is not None, "Index 'idx_orders_status_date' does not exist."
    assert index_info[1] == 'orders', "Index 'idx_orders_status_date' is not on the 'orders' table."

    # Check the columns of the index
    cursor.execute("PRAGMA index_info('idx_orders_status_date');")
    columns = [row[2] for row in cursor.fetchall()]
    assert len(columns) == 2, f"Index should have 2 columns, found {len(columns)}."
    assert columns[0] == 'status', f"First column in index should be 'status', found '{columns[0]}'."
    assert columns[1] == 'created_at', f"Second column in index should be 'created_at', found '{columns[1]}'."

    conn.close()

def test_explain_query_plan_output():
    """Verify that the EXPLAIN QUERY PLAN output was saved and uses the index."""
    assert os.path.exists(PLAN_PATH), f"Plan output file {PLAN_PATH} is missing."

    with open(PLAN_PATH, 'r') as f:
        plan_content = f.read()

    assert "idx_orders_status_date" in plan_content, "The query plan in plan.txt does not show usage of 'idx_orders_status_date'."

def test_json_export_structure_and_data():
    """Verify the exported JSON file has the correct structure and data."""
    assert os.path.exists(JSON_PATH), f"JSON export file {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON root should be an array (list)."
    assert len(data) == 20, f"Expected 20 items in the JSON array, found {len(data)}."

    expected_keys = {"order_id", "customer_name", "customer_email", "order_total", "order_date"}

    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {i} is not a JSON object."
        item_keys = set(item.keys())
        assert item_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {item_keys}."

        # Check types
        assert isinstance(item["order_id"], int), f"order_id at index {i} should be an integer."
        assert isinstance(item["customer_name"], str), f"customer_name at index {i} should be a string."
        assert isinstance(item["customer_email"], str), f"customer_email at index {i} should be a string."
        assert isinstance(item["order_total"], (int, float)), f"order_total at index {i} should be a float."
        assert isinstance(item["order_date"], str), f"order_date at index {i} should be a string."

def test_json_data_correctness():
    """Verify the JSON data matches the actual expected query results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT orders.id, customers.name, customers.email, orders.total, orders.created_at 
    FROM orders 
    JOIN customers ON orders.customer_id = customers.id 
    WHERE orders.status = 'pending' 
    ORDER BY orders.created_at DESC 
    LIMIT 20;
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    with open(JSON_PATH, 'r') as f:
        data = json.load(f)

    for i, (expected, actual) in enumerate(zip(expected_rows, data)):
        assert actual["order_id"] == expected[0], f"Mismatch in order_id at index {i}."
        assert actual["customer_name"] == expected[1], f"Mismatch in customer_name at index {i}."
        assert actual["customer_email"] == expected[2], f"Mismatch in customer_email at index {i}."
        assert abs(actual["order_total"] - expected[3]) < 0.01, f"Mismatch in order_total at index {i}."
        assert actual["order_date"] == expected[4], f"Mismatch in order_date at index {i}."