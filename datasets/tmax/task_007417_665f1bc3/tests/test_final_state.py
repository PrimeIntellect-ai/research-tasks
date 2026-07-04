# test_final_state.py
import os
import json
import sqlite3
import pytest

SCRIPT_PATH = '/home/user/analyze_high_value_users.py'
REPORT_PATH = '/home/user/report.json'
DB_PATH = '/home/user/ecommerce.db'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Expected a file at {SCRIPT_PATH}"

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report missing at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Expected a file at {REPORT_PATH}"

def test_report_contents():
    # Dynamically compute expected results from the database
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    target_year = 2022

    # Query 1: users in target_year
    c.execute("SELECT user_id FROM users WHERE reg_year = ?", (target_year,))
    user_ids = [row[0] for row in c.fetchall()]
    expected_users_count = len(user_ids)

    # Query 2: orders for those users with total > 100
    if not user_ids:
        expected_orders_count = 0
        order_ids = []
    else:
        placeholders = ','.join('?' * len(user_ids))
        c.execute(f"SELECT order_id FROM orders WHERE user_id IN ({placeholders}) AND total > 100.0", user_ids)
        order_ids = [row[0] for row in c.fetchall()]
        expected_orders_count = len(order_ids)

    # Query 3: order items for those orders in 'Electronics'
    if not order_ids:
        expected_spend = 0.0
        expected_qty = 0
    else:
        placeholders = ','.join('?' * len(order_ids))
        c.execute(f"SELECT SUM(price * quantity), SUM(quantity) FROM order_items WHERE order_id IN ({placeholders}) AND category = 'Electronics'", order_ids)
        row = c.fetchone()
        expected_spend = float(row[0]) if row[0] is not None else 0.0
        expected_qty = int(row[1]) if row[1] is not None else 0

    conn.close()

    # Read and validate the report
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "target_year" in report, "Missing 'target_year' in report"
    assert report["target_year"] == target_year, f"Expected target_year {target_year}, got {report['target_year']}"

    assert "eligible_users_count" in report, "Missing 'eligible_users_count' in report"
    assert report["eligible_users_count"] == expected_users_count, f"Expected {expected_users_count} eligible users, got {report['eligible_users_count']}"

    assert "eligible_orders_count" in report, "Missing 'eligible_orders_count' in report"
    assert report["eligible_orders_count"] == expected_orders_count, f"Expected {expected_orders_count} eligible orders, got {report['eligible_orders_count']}"

    assert "total_electronics_spend" in report, "Missing 'total_electronics_spend' in report"
    assert float(report["total_electronics_spend"]) == expected_spend, f"Expected total_electronics_spend {expected_spend}, got {report['total_electronics_spend']}"

    assert "total_electronics_quantity" in report, "Missing 'total_electronics_quantity' in report"
    assert int(report["total_electronics_quantity"]) == expected_qty, f"Expected total_electronics_quantity {expected_qty}, got {report['total_electronics_quantity']}"