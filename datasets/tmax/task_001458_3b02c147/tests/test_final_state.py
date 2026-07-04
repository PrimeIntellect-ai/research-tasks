# test_final_state.py
import json
import sqlite3
import os
import pytest

def test_validation_summary_exists():
    assert os.path.exists('/home/user/validation_summary.json'), "The output file /home/user/validation_summary.json does not exist."

def test_validation_summary_metrics():
    summary_path = '/home/user/validation_summary.json'
    assert os.path.isfile(summary_path), f"File not found: {summary_path}"

    try:
        with open(summary_path, 'r') as f:
            agent_data = {row['customer_id']: row for row in json.load(f)}
    except Exception as e:
        pytest.fail(f"Failed to read agent output: {e}")

    db_path = '/home/user/backup.db'
    assert os.path.exists(db_path), f"The database at {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    SELECT c.customer_id, 
           COALESCE((SELECT SUM(o.amount) FROM orders o WHERE o.customer_id = c.customer_id), 0) as total_order_amount,
           COALESCE((SELECT COUNT(i.item_id) FROM items i JOIN orders o ON i.order_id = o.order_id WHERE o.customer_id = c.customer_id), 0) as total_items
    FROM customers c
    """)
    expected_rows = c.fetchall()

    mae_sum = 0.0
    count = 0

    for row in expected_rows:
        cid, exp_amount, exp_items = row
        if cid not in agent_data:
            mae_sum += 99999.0
            count += 1
            continue

        agent_row = agent_data[cid]
        amount_diff = abs(exp_amount - float(agent_row.get('total_order_amount', 0)))
        items_diff = abs(exp_items - int(agent_row.get('total_items', 0)))

        mae_sum += amount_diff + items_diff
        count += 1

    mae = mae_sum / max(count, 1)

    assert mae <= 0.01, f"Expected MAE <= 0.01, but got {mae}. The aggregates in validation_summary.json are incorrect."