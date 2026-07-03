# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/ecommerce.db'
OPTIMIZE_PY_PATH = '/home/user/optimize.py'
JSON_OUTPUT_PATH = '/home/user/top_customers.json'
QUERY_PLAN_PATH = '/home/user/query_plan.txt'

def test_optimize_script_exists():
    assert os.path.exists(OPTIMIZE_PY_PATH), f"Script missing at {OPTIMIZE_PY_PATH}"
    assert os.path.isfile(OPTIMIZE_PY_PATH), f"{OPTIMIZE_PY_PATH} is not a file"

def test_index_created():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Check for any index on the orders table
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='orders';")
    indexes = cursor.fetchall()
    conn.close()

    # Exclude auto-indexes created by sqlite for primary keys if any, though usually they don't show up this way
    user_indexes = [idx for idx in indexes if idx[1] is not None]
    assert len(user_indexes) > 0, "No custom index was created on the 'orders' table."

    # Ideally, the index should be on customer_id. We can check if 'customer_id' is in the SQL definition.
    index_sql = " ".join([idx[1].lower() for idx in user_indexes])
    assert "customer_id" in index_sql, "The created index does not appear to be on 'customer_id'."

def test_top_customers_json():
    assert os.path.exists(JSON_OUTPUT_PATH), f"JSON output missing at {JSON_OUTPUT_PATH}"

    with open(JSON_OUTPUT_PATH, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_OUTPUT_PATH} does not contain valid JSON.")

    # Compute the expected result directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.name, SUM(o.amount) as total_amount, RANK() OVER(ORDER BY SUM(o.amount) DESC) as rank
        FROM customers c JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id
        ORDER BY rank LIMIT 5
    ''')

    expected = [{"name": row[0], "total_amount": row[1], "rank": row[2]} for row in cursor.fetchall()]
    conn.close()

    assert isinstance(actual, list), "JSON output should be a list of dictionaries."
    assert len(actual) == len(expected), f"Expected {len(expected)} items, got {len(actual)}."

    for i in range(len(expected)):
        assert actual[i].get("name") == expected[i]["name"], f"Mismatch in name at rank {i+1}"
        assert abs(actual[i].get("total_amount", 0) - expected[i]["total_amount"]) < 1e-5, f"Mismatch in total_amount at rank {i+1}"
        assert actual[i].get("rank") == expected[i]["rank"], f"Mismatch in rank at rank {i+1}"

def test_query_plan_txt():
    assert os.path.exists(QUERY_PLAN_PATH), f"Query plan output missing at {QUERY_PLAN_PATH}"

    with open(QUERY_PLAN_PATH, 'r') as f:
        content = f.read().upper()

    assert content.strip(), "Query plan file is empty."

    # Check for common EXPLAIN QUERY PLAN keywords
    has_scan = "SCAN" in content
    has_search = "SEARCH" in content
    has_covering = "COVERING INDEX" in content

    assert has_scan or has_search or has_covering, "Query plan output does not contain expected EXPLAIN QUERY PLAN keywords (SCAN, SEARCH, etc.)."