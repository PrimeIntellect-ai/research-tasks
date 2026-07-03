# test_final_state.py

import os
import csv
import sqlite3
import pytest

def test_results_csv():
    results_path = '/home/user/results.csv'
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 3, "Results CSV should have a header and at least 2 data rows."
    assert rows[0] == ['name', 'total_spent'], "CSV header is incorrect."

    # Convert rows to a dictionary for easy checking, ignoring header
    results_dict = {}
    for row in rows[1:]:
        if len(row) == 2:
            results_dict[row[0]] = float(row[1])

    assert 'Alice' in results_dict, "Alice's results are missing."
    assert results_dict['Alice'] == 1050.0, f"Alice's total spent is incorrect. Expected 1050.0, got {results_dict['Alice']}"

    assert 'Bob' in results_dict, "Bob's results are missing."
    assert results_dict['Bob'] == 1000.0, f"Bob's total spent is incorrect. Expected 1000.0, got {results_dict['Bob']}"

def test_database_indexes():
    db_path = '/home/user/store.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Check users table indexes
    c.execute("PRAGMA index_list('users');")
    user_indexes = c.fetchall()
    has_status_index = False
    for idx in user_indexes:
        c.execute(f"PRAGMA index_info('{idx[1]}');")
        cols = [row[2] for row in c.fetchall()]
        if 'status' in cols:
            has_status_index = True
            break

    assert has_status_index, "Missing index on 'status' column in 'users' table."

    # Check products table indexes
    c.execute("PRAGMA index_list('products');")
    product_indexes = c.fetchall()
    has_category_index = False
    for idx in product_indexes:
        c.execute(f"PRAGMA index_info('{idx[1]}');")
        cols = [row[2] for row in c.fetchall()]
        if 'category' in cols:
            has_category_index = True
            break

    assert has_category_index, "Missing index on 'category' column in 'products' table."
    conn.close()

def test_plan_txt():
    plan_path = '/home/user/plan.txt'
    assert os.path.isfile(plan_path), f"Query plan file {plan_path} is missing."

    with open(plan_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, "The plan.txt file is empty."
    # A typical EXPLAIN QUERY PLAN output contains words like SCAN, SEARCH, or USE TEMP B-TREE
    assert any(keyword in content.upper() for keyword in ['SCAN', 'SEARCH', 'LIST', 'COROUTINE', 'B-TREE']), "The plan.txt file does not look like a valid EXPLAIN QUERY PLAN output."

def test_analyze_py_uses_explicit_join():
    script_path = '/home/user/analyze.py'
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read().upper()

    assert ' JOIN ' in content, "The query does not seem to use explicit JOIN syntax."