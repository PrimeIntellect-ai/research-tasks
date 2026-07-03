# test_final_state.py
import os
import sqlite3
import json
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_backup.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_report_exists_and_valid_json():
    report_path = "/home/user/integrity_report.json"
    assert os.path.isfile(report_path), f"Report not found at {report_path}"
    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report is not valid JSON")

    assert "orphaned_orders_count" in data, "Missing 'orphaned_orders_count' in report"
    assert "orphaned_orders_amount" in data, "Missing 'orphaned_orders_amount' in report"
    assert "orphaned_payments_count" in data, "Missing 'orphaned_payments_count' in report"
    assert "orphaned_payments_amount" in data, "Missing 'orphaned_payments_amount' in report"

def test_report_content_matches_db():
    db_path = "/home/user/db_backup.sqlite"
    report_path = "/home/user/integrity_report.json"

    assert os.path.isfile(db_path), f"Database not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate truth dynamically using PRAGMA foreign_key_check
    cursor.execute("PRAGMA foreign_key_check;")
    violations = cursor.fetchall()

    orphaned_orders_ids = [row[1] for row in violations if row[0] == 'orders']
    orphaned_payments_ids = [row[1] for row in violations if row[0] == 'payments']

    orders_count = len(orphaned_orders_ids)
    payments_count = len(orphaned_payments_ids)

    orders_amount = 0.0
    if orphaned_orders_ids:
        placeholders = ','.join('?' * len(orphaned_orders_ids))
        cursor.execute(f"SELECT SUM(amount) FROM orders WHERE id IN ({placeholders})", orphaned_orders_ids)
        orders_amount = cursor.fetchone()[0] or 0.0

    payments_amount = 0.0
    if orphaned_payments_ids:
        placeholders = ','.join('?' * len(orphaned_payments_ids))
        cursor.execute(f"SELECT SUM(amount) FROM payments WHERE id IN ({placeholders})", orphaned_payments_ids)
        payments_amount = cursor.fetchone()[0] or 0.0

    conn.close()

    with open(report_path, "r") as f:
        data = json.load(f)

    assert data["orphaned_orders_count"] == orders_count, f"Expected {orders_count} orphaned orders"
    assert float(data["orphaned_orders_amount"]) == pytest.approx(orders_amount, 0.01), "Orphaned orders amount mismatch"
    assert data["orphaned_payments_count"] == payments_count, f"Expected {payments_count} orphaned payments"
    assert float(data["orphaned_payments_amount"]) == pytest.approx(payments_amount, 0.01), "Orphaned payments amount mismatch"

    # Check formatting for 2 decimal places
    with open(report_path, "r") as f:
        raw_content = f.read()

    assert re.search(r'"orphaned_orders_amount"\s*:\s*\d+\.\d{2}(?!\d)', raw_content), "orphaned_orders_amount is not formatted to exactly 2 decimal places"
    assert re.search(r'"orphaned_payments_amount"\s*:\s*\d+\.\d{2}(?!\d)', raw_content), "orphaned_payments_amount is not formatted to exactly 2 decimal places"