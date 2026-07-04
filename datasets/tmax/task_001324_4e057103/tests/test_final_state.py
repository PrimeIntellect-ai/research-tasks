# test_final_state.py
import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/sales.db"
REPORT_PATH = "/home/user/report.csv"

def test_sales_db_exists():
    """Check if the SQLite database was created."""
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} is missing."

def test_sales_db_schema():
    """Check if the normalized tables exist in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    expected_tables = {"users", "products", "transactions"}
    for table in expected_tables:
        assert table in tables, f"Table '{table}' is missing from the database."

    conn.close()

def test_sales_db_indexes():
    """Check if indexes were created."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    indexes = cursor.fetchall()

    assert len(indexes) > 0, "No indexes were found in the database. You must create appropriate indexes."

    conn.close()

def test_report_csv_exists():
    """Check if the report CSV file was created."""
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} is missing."

def test_report_csv_content():
    """Check if the report CSV has the correct content."""
    expected_data = [
        ["Category", "TotalRevenue"],
        ["Electronics", "4050.00"],
        ["Furniture", "1200.00"],
        ["Media", "200.00"]
    ]

    with open(REPORT_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = [row for row in reader if row] # ignore empty lines

    assert actual_data == expected_data, f"The contents of {REPORT_PATH} do not match the expected output."