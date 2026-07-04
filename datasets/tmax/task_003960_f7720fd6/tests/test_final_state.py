# test_final_state.py

import os
import sqlite3
import csv
import pytest

def test_retail_db_exists():
    db_path = '/home/user/retail.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

def test_database_has_indexes():
    db_path = '/home/user/retail.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count > 0, "No custom indexes found in the database. You must create necessary indexes to optimize query performance."

def test_indexes_sql_exists():
    sql_path = '/home/user/indexes.sql'
    assert os.path.isfile(sql_path), f"SQL file {sql_path} is missing."

def test_analyze_script_exists():
    script_path = '/home/user/analyze.py'
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

def test_electronics_trailing_revenue_csv():
    csv_path = '/home/user/electronics_trailing_revenue.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    expected_rows = [
        ["product_id", "product_name", "sale_date", "daily_revenue", "trailing_7_sales_revenue"],
        ["101", "MacBook Pro", "2023-10-01", "2000", "6000"],
        ["101", "MacBook Pro", "2023-10-02", "4000", "10000"],
        ["101", "MacBook Pro", "2023-10-05", "2000", "12000"],
        ["101", "MacBook Pro", "2023-10-20", "2000", "14000"],
        ["102", "iPhone 14", "2023-10-01", "5000", "5000"],
        ["104", "Desktop PC", "2023-10-15", "1500", "1500"]
    ]

    actual_rows = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # strip whitespace from each cell just in case
            actual_rows.append([cell.strip() for cell in row])

    assert len(actual_rows) > 0, f"The file {csv_path} is empty."
    assert actual_rows[0] == expected_rows[0], f"Header row in {csv_path} is incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}"

    assert actual_rows == expected_rows, f"The contents of {csv_path} do not match the expected output. Expected: {expected_rows}, Actual: {actual_rows}"