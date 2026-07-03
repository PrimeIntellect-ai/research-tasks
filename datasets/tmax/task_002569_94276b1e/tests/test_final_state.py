# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/ecommerce.db'
OUTPUT_PATH = '/home/user/output.json'

def test_indexes_created():
    """Verify that at least 4 secondary indexes were created in the database."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) >= 4, f"Expected at least 4 secondary indexes to be created, but found {len(indexes)}: {indexes}"

def test_output_json_correct():
    """Verify that the output.json file exists, is valid JSON, and contains the correct sorted data."""
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not found."

    with open(OUTPUT_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(actual_data, list), f"Expected the JSON output to be a list of objects, got {type(actual_data).__name__}."

    # Derive the expected data directly from the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = '''
        SELECT 
            u.name AS user_name, 
            u.email, 
            o.order_date, 
            p.name AS product_name, 
            oi.quantity
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE p.category = ? AND o.order_date BETWEEN ? AND ?
        ORDER BY o.order_date ASC, p.name ASC, u.name ASC
    '''

    # Using the parameters specified in the task
    cursor.execute(query, ('Electronics', '2023-01-01', '2023-12-31'))
    expected_data = [dict(row) for row in cursor.fetchall()]
    conn.close()

    assert actual_data == expected_data, (
        "The contents of output.json do not match the expected query results. "
        "Ensure you are joining the correct tables, filtering by the exact category and date range, "
        "and sorting by order_date ASC, product_name ASC, user_name ASC."
    )