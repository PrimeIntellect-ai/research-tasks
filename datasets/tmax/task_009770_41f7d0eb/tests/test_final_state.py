# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/ecommerce.db"
SCRIPT_PATH = "/home/user/get_orders.sh"

def test_index_exists_and_optimizes_query():
    """Verify that an index exists and prevents full table scans for the target query."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    query = "EXPLAIN QUERY PLAN SELECT order_id, order_date, amount FROM orders WHERE customer_id = 'CUST_A' AND status = 'SHIPPED' ORDER BY order_date DESC;"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    plan = cursor.fetchall()
    conn.close()

    plan_text = " ".join([row[-1] for row in plan]).upper()

    assert "SEARCH" in plan_text, "The query plan does not use an index (SEARCH missing)."
    assert "SCAN" not in plan_text, "The query plan still performs a full table SCAN."

def test_script_exists_and_executable():
    """Verify the bash script exists and has executable permissions."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_output_and_pagination():
    """Verify the script outputs correct CSV data and handles pagination."""
    # Test offset 0
    result1 = subprocess.run([SCRIPT_PATH, "CUST_A", "SHIPPED", "1", "0"], capture_output=True, text=True)
    assert result1.returncode == 0, "Script failed with offset 0."

    expected_output1 = "order_id,order_date,amount\nORD003,2023-10-03T12:00:00Z,99.99\n"
    assert result1.stdout.strip() == expected_output1.strip(), "Script output mismatch for offset 0."

    # Test offset 1
    result2 = subprocess.run([SCRIPT_PATH, "CUST_A", "SHIPPED", "1", "1"], capture_output=True, text=True)
    assert result2.returncode == 0, "Script failed with offset 1."

    expected_output2 = "order_id,order_date,amount\nORD001,2023-10-01T10:00:00Z,150.5\n"
    # Allow 150.50 or 150.5
    assert result2.stdout.strip() in (expected_output2.strip(), expected_output2.strip() + "0"), "Script output mismatch for offset 1."

def test_script_integer_validation():
    """Verify the script validates limit and offset as integers."""
    result = subprocess.run([SCRIPT_PATH, "CUST_A", "SHIPPED", "1 DROP TABLE orders;", "0"], capture_output=True, text=True)
    assert result.returncode != 0, "Script did not fail when given a non-integer limit."

def test_script_contains_timeout():
    """Verify the script configures a busy timeout."""
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read().lower()

    assert "timeout" in content, "Script does not contain timeout configuration."