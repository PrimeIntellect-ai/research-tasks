# test_final_state.py
import os
import sqlite3
import json
import subprocess
import pytest

DB_PATH = '/home/user/logistics.db'
RUN_REPORT_PATH = '/home/user/run_report.sh'
INDEXES_SQL_PATH = '/home/user/indexes.sql'
OPTIMIZED_SQL_PATH = '/home/user/optimized.sql'

def get_expected_results(limit, offset):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = """
    SELECT 
        c.id as customer_id,
        c.name as customer_name,
        SUM(oi.price) as total_revenue,
        MAX(o.order_date) as latest_order_date,
        SUM(CASE WHEN s.status = 'DELAYED' THEN 1 ELSE 0 END) as delayed_shipment_count
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN shipments s ON o.id = s.order_id
    GROUP BY c.id
    HAVING delayed_shipment_count > 0
    ORDER BY total_revenue DESC, customer_id ASC
    LIMIT ? OFFSET ?
    """
    c.execute(query, (limit, offset))
    rows = [dict(row) for row in c.fetchall()]
    for r in rows:
        r['total_revenue'] = round(r['total_revenue'], 2)
    conn.close()
    return rows

def test_files_exist():
    assert os.path.exists(INDEXES_SQL_PATH), f"Missing {INDEXES_SQL_PATH}"
    assert os.path.exists(OPTIMIZED_SQL_PATH), f"Missing {OPTIMIZED_SQL_PATH}"

def test_run_report_exists_and_executable():
    assert os.path.exists(RUN_REPORT_PATH), f"Missing {RUN_REPORT_PATH}"
    assert os.access(RUN_REPORT_PATH, os.X_OK), f"{RUN_REPORT_PATH} is not executable"

def test_indexes_created():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    index_count = c.fetchone()[0]
    conn.close()

    assert index_count >= 1, "No new indexes were created in the database."

def test_run_report_output_format_and_correctness():
    limit, offset = 5, 0
    expected = get_expected_results(limit, offset)

    result = subprocess.run([RUN_REPORT_PATH, str(limit), str(offset)], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Output was: {result.stdout[:100]}...")

    assert isinstance(output, list), "Output should be a JSON array"
    assert len(output) == len(expected), f"Expected {len(expected)} results, got {len(output)}"

    for i, (out_row, exp_row) in enumerate(zip(output, expected)):
        assert int(out_row.get('customer_id', -1)) == exp_row['customer_id'], f"Row {i}: customer_id mismatch"
        assert out_row.get('customer_name') == exp_row['customer_name'], f"Row {i}: customer_name mismatch"
        assert round(float(out_row.get('total_revenue', 0)), 2) == exp_row['total_revenue'], f"Row {i}: total_revenue mismatch"
        assert out_row.get('latest_order_date') == exp_row['latest_order_date'], f"Row {i}: latest_order_date mismatch"
        assert int(out_row.get('delayed_shipment_count', -1)) == exp_row['delayed_shipment_count'], f"Row {i}: delayed_shipment_count mismatch"

def test_run_report_pagination():
    limit, offset = 3, 2
    expected = get_expected_results(limit, offset)

    result = subprocess.run([RUN_REPORT_PATH, str(limit), str(offset)], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON on pagination test")

    assert len(output) == len(expected), f"Pagination failed: Expected {len(expected)} results, got {len(output)}"

    if expected:
        assert int(output[0].get('customer_id', -1)) == expected[0]['customer_id'], "Pagination returned incorrect starting record"