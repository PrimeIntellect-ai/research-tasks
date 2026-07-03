# test_final_state.py
import os
import sqlite3
import subprocess
import csv
import ast
import pytest

FIXED_ETL_PATH = '/home/user/fixed_etl.py'
INDEXES_SQL_PATH = '/home/user/indexes.sql'
OUTPUT_CSV_PATH = '/home/user/output.csv'
QUERY_PLAN_PATH = '/home/user/query_plan.txt'
DB_PATH = '/home/user/etl_data.db'

def test_fixed_etl_exists_and_parameterized():
    assert os.path.exists(FIXED_ETL_PATH), f"File {FIXED_ETL_PATH} does not exist."

    with open(FIXED_ETL_PATH, 'r') as f:
        content = f.read()

    # Check for parameterization markers
    has_qmark = '?' in content
    has_named = ':' in content
    has_format = '.format(' in content

    assert has_qmark or has_named, "The corrected script does not appear to use parameterized queries (missing '?' or ':name' markers)."

    # Parse AST to check if f-strings are used for queries. 
    # We can't strictly ban all f-strings, but we can check if they are used in cursor.execute
    class ExecuteVisitor(ast.NodeVisitor):
        def __init__(self):
            self.uses_fstring = False

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                if node.args and isinstance(node.args[0], ast.JoinedStr):
                    self.uses_fstring = True
            self.generic_visit(node)

    try:
        tree = ast.parse(content)
        visitor = ExecuteVisitor()
        visitor.visit(tree)
        assert not visitor.uses_fstring, "The script still uses f-strings in cursor.execute(), making it vulnerable to SQL injection."
    except SyntaxError:
        pytest.fail(f"Syntax error in {FIXED_ETL_PATH}")

def test_indexes_sql_applied():
    assert os.path.exists(INDEXES_SQL_PATH), f"File {INDEXES_SQL_PATH} does not exist."

    with open(INDEXES_SQL_PATH, 'r') as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute the DDL script
    try:
        cursor.executescript(sql_script)
    except Exception as e:
        pytest.fail(f"Failed to execute indexes.sql: {e}")

    # Verify an index was created on purchases or users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name IN ('purchases', 'users');")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes were created on 'purchases' or 'users' tables."

    conn.close()

def test_fixed_etl_execution_and_output():
    # Run the script with the test arguments
    result = subprocess.run(
        ['python3', FIXED_ETL_PATH, '2023-01-10', '2023-02-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    assert os.path.exists(OUTPUT_CSV_PATH), f"Output file {OUTPUT_CSV_PATH} was not created."

    expected_rows = [
        {'name': 'Bob', 'amount': '100.0', 'purchase_date': '2023-02-15'},
        {'name': 'Charlie', 'amount': '75.0', 'purchase_date': '2023-01-25'}
    ]

    actual_rows = []
    with open(OUTPUT_CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['name', 'amount', 'purchase_date'], "CSV headers do not match expected."
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == 2, f"Expected 2 rows in output, got {len(actual_rows)}."

    # Sort both to compare regardless of order
    expected_sorted = sorted(expected_rows, key=lambda x: x['name'])
    actual_sorted = sorted(actual_rows, key=lambda x: x['name'])

    assert actual_sorted == expected_sorted, f"CSV contents do not match expected. Got: {actual_sorted}"

def test_query_plan_exists():
    assert os.path.exists(QUERY_PLAN_PATH), f"File {QUERY_PLAN_PATH} does not exist."

    with open(QUERY_PLAN_PATH, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"{QUERY_PLAN_PATH} is empty."

    content_upper = content.upper()
    assert "SCAN" in content_upper or "SEARCH" in content_upper, f"{QUERY_PLAN_PATH} does not look like standard EXPLAIN QUERY PLAN output."