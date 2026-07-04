# test_final_state.py

import os
import sqlite3
import csv

DB_PATH = "/home/user/supply_chain.db"
CSV_PATH = "/home/user/materials_needed.csv"

def test_database_and_indexes():
    """Verify that the SQLite database exists and has appropriate indexes."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No indexes found in the database."

    tables_with_indexes = set(tbl_name.lower() for name, tbl_name in indexes)

    # The requirement specifically asks for indexes on the 'bom' table and 'items' table.
    # SQLite auto-creates indexes for PRIMARY KEY, but we just check if any index is present for both tables.
    assert 'bom' in tables_with_indexes, "No index found on the 'bom' table for optimizing downward graph traversal."
    assert 'items' in tables_with_indexes, "No index found on the 'items' table for fast primary key lookups."

def test_materials_needed_csv():
    """Verify that the output CSV exists, has the correct header, sorted rows, and accurate calculations."""
    assert os.path.isfile(CSV_PATH), f"Output file {CSV_PATH} does not exist."

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    expected_header = ["leaf_item_id", "leaf_item_name", "total_quantity_needed"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    data_rows = rows[1:]

    expected_data = [
        ["RAW-1", "SteelSheet", "300"],
        ["RAW-2", "SiliconWafer", "800"],
        ["RAW-3", "CopperWire", "250"]
    ]

    leaf_ids = [row[0] for row in data_rows if len(row) > 0]
    assert leaf_ids == sorted(leaf_ids), "Data rows are not sorted alphabetically by leaf_item_id."

    assert data_rows == expected_data, f"Expected data {expected_data}, but got {data_rows}."