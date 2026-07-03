# test_final_state.py

import os
import csv
import sqlite3
import pytest

DB_PATH = '/home/user/ecommerce.db'
REPORT_PATH = '/home/user/report.csv'

EXPECTED_CSV_DATA = [
    ['base_product_id', 'accessory_product_id', 'sale_date', 'daily_total', 'rolling_3d_avg'],
    ['B1', 'A1', '2023-10-01', '25.0', '25.0'],
    ['B1', 'A1', '2023-10-02', '20.0', '22.5'],
    ['B1', 'A1', '2023-10-03', '30.0', '25.0'],
    ['B1', 'A1', '2023-10-04', '10.0', '20.0'],
    ['B1', 'A2', '2023-10-01', '50.0', '50.0'],
    ['B1', 'A2', '2023-10-03', '60.0', '55.0'],
    ['B2', 'A3', '2023-10-01', '100.0', '100.0']
]

def test_report_csv_exists_and_content():
    """Verify that the report.csv exists and contains the exact expected data."""
    assert os.path.exists(REPORT_PATH), f"Output file missing at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file"

    with open(REPORT_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert len(actual_data) > 0, "The report.csv file is empty"

    # Check headers
    assert actual_data[0] == EXPECTED_CSV_DATA[0], f"Headers do not match expected. Got: {actual_data[0]}"

    # Check rows
    assert len(actual_data) == len(EXPECTED_CSV_DATA), f"Expected {len(EXPECTED_CSV_DATA)} rows, got {len(actual_data)}"

    for i, (actual_row, expected_row) in enumerate(zip(actual_data[1:], EXPECTED_CSV_DATA[1:]), start=1):
        assert actual_row == expected_row, f"Row {i} mismatch. Expected: {expected_row}, Got: {actual_row}"

def test_database_indexes():
    """Verify that at least one index was created for both 'sales' and 'product_graph' tables."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check indexes for sales table
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='sales' AND name NOT LIKE 'sqlite_autoindex%';")
    sales_indexes = cur.fetchone()[0]
    assert sales_indexes >= 1, "No explicit indexes found for the 'sales' table."

    # Check indexes for product_graph table
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='product_graph' AND name NOT LIKE 'sqlite_autoindex%';")
    graph_indexes = cur.fetchone()[0]
    assert graph_indexes >= 1, "No explicit indexes found for the 'product_graph' table."

    conn.close()