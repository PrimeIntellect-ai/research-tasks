# test_final_state.py

import os
import sqlite3
import pytest

def test_extracted_csv_exists():
    csv_path = "/home/user/transactions.csv"
    assert os.path.isfile(csv_path), f"Expected extracted file {csv_path} is missing."

def test_database_and_data():
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Expected database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='category_metrics';")
    assert cursor.fetchone() is not None, "Table 'category_metrics' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(category_metrics);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        "category": "TEXT",
        "total_volume": "INTEGER",
        "total_value": "REAL",
        "vwap": "REAL"
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from 'category_metrics'."
        # SQLite types can sometimes be flexible, but we check if it starts with the expected type
        assert columns[col].startswith(col_type), f"Column '{col}' has type {columns[col]}, expected {col_type}."

    # Check data and sorting
    cursor.execute("SELECT category, total_volume, total_value, vwap FROM category_metrics;")
    rows = cursor.fetchall()

    expected_rows = [
        ("Alpha", 150, 1650.00, 11.00),
        ("Beta", 300, 1450.00, 4.83),
        ("Delta", 60, 1000.00, 16.67),
        ("Gamma", 10, 1000.00, 100.00)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected category {expected[0]}, got {actual[0]}. (Check sorting or parsing)"
        assert actual[1] == expected[1], f"Row {i+1} ({actual[0]}): Expected total_volume {expected[1]}, got {actual[1]}."
        assert abs(actual[2] - expected[2]) < 0.001, f"Row {i+1} ({actual[0]}): Expected total_value {expected[2]}, got {actual[2]}."
        assert abs(actual[3] - expected[3]) < 0.001, f"Row {i+1} ({actual[0]}): Expected vwap {expected[3]}, got {actual[3]}."

    conn.close()

def test_sql_export_exists():
    sql_path = "/home/user/export.sql"
    assert os.path.isfile(sql_path), f"Expected SQL export file {sql_path} is missing."

    with open(sql_path, "r") as f:
        content = f.read()
        assert "CREATE TABLE" in content and "category_metrics" in content, "The SQL export file does not appear to contain the dump of 'category_metrics'."
        assert "INSERT INTO" in content, "The SQL export file does not appear to contain the data inserts."