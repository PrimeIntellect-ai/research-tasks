# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/etl_data.db'
JSON_PATH = '/home/user/aggregated_sales.json'

def compute_expected_aggregates(db_path):
    """
    Computes the expected hierarchical sales aggregates directly from the database
    to ensure the test is aligned with the ground truth logically.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT emp_id, manager_id, sales_amount, updated_at FROM sales_raw")
    rows = c.fetchall()
    conn.close()

    # 1. Deduplicate: keep the record with the most recent updated_at for each emp_id
    latest_records = {}
    for emp_id, manager_id, sales_amount, updated_at in rows:
        if emp_id not in latest_records:
            latest_records[emp_id] = (manager_id, sales_amount, updated_at)
        else:
            # Compare timestamps string-wise (ISO 8601 format allows this)
            if updated_at > latest_records[emp_id][2]:
                latest_records[emp_id] = (manager_id, sales_amount, updated_at)

    # 2. Build adjacency list for the hierarchy
    children = {}
    sales = {}
    for emp_id, (manager_id, sales_amount, _) in latest_records.items():
        sales[emp_id] = sales_amount
        if manager_id not in children:
            children[manager_id] = []
        children[manager_id].append(emp_id)

    # 3. Recursive function to calculate inclusive sales
    def get_inclusive_sales(eid):
        total = sales[eid]
        for child_id in children.get(eid, []):
            total += get_inclusive_sales(child_id)
        return total

    # 4. Format expected output
    expected = []
    for emp_id in sorted(sales.keys()):
        expected.append({
            "emp_id": emp_id,
            "total_inclusive_sales": get_inclusive_sales(emp_id)
        })
    return expected

def test_json_exists():
    assert os.path.exists(JSON_PATH), f"Output file missing at {JSON_PATH}. Did your script generate it?"
    assert os.path.isfile(JSON_PATH), f"Expected a file at {JSON_PATH}, but found a directory."

def test_json_contents():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}. Do not delete the database."
    expected = compute_expected_aggregates(DB_PATH)

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file at {JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON output must be a list of objects (dictionaries)."
    assert len(data) == len(expected), f"Expected {len(expected)} records in the JSON, got {len(data)}."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected)):
        assert isinstance(actual_row, dict), f"Record at index {i} is not a JSON object."
        assert "emp_id" in actual_row, f"Record at index {i} is missing the 'emp_id' key."
        assert "total_inclusive_sales" in actual_row, f"Record at index {i} is missing the 'total_inclusive_sales' key."

        assert actual_row["emp_id"] == expected_row["emp_id"], \
            f"Record at index {i} expected emp_id {expected_row['emp_id']}, got {actual_row['emp_id']}."

        assert actual_row["total_inclusive_sales"] == expected_row["total_inclusive_sales"], \
            f"Incorrect total_inclusive_sales for emp_id {expected_row['emp_id']}. " \
            f"Expected {expected_row['total_inclusive_sales']}, got {actual_row['total_inclusive_sales']}."