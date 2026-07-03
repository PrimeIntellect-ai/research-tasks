# test_final_state.py
import os
import sqlite3
import csv
import pytest

def test_files_exist():
    expected_files = [
        "/home/user/build_db.py",
        "/home/user/store.db",
        "/home/user/indexes.sql",
        "/home/user/query.sql",
        "/home/user/top_spenders.csv"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} is missing."

def test_database_schema():
    db_path = "/home/user/store.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    expected_tables = {"clients", "items", "purchases", "purchase_lines"}
    assert expected_tables.issubset(tables), f"Database is missing expected tables. Found: {tables}"

    # Check Foreign Keys for purchases table
    cursor.execute("PRAGMA foreign_key_list(purchases);")
    purchases_fks = cursor.fetchall()
    assert len(purchases_fks) >= 1, "No foreign keys defined for 'purchases' table."
    # purchases.c_ref -> clients.c_id
    fk_clients = [fk for fk in purchases_fks if fk[2] == "clients"]
    assert fk_clients, "No foreign key referencing 'clients' found in 'purchases' table."

    # Check Foreign Keys for purchase_lines table
    cursor.execute("PRAGMA foreign_key_list(purchase_lines);")
    lines_fks = cursor.fetchall()
    assert len(lines_fks) >= 2, "Expected at least 2 foreign keys in 'purchase_lines' table."

    fk_purchases = [fk for fk in lines_fks if fk[2] == "purchases"]
    fk_items = [fk for fk in lines_fks if fk[2] == "items"]

    assert fk_purchases, "No foreign key referencing 'purchases' found in 'purchase_lines' table."
    assert fk_items, "No foreign key referencing 'items' found in 'purchase_lines' table."

    conn.close()

def test_indexes_created():
    sql_path = "/home/user/indexes.sql"
    assert os.path.isfile(sql_path), f"File {sql_path} does not exist."

    with open(sql_path, 'r') as f:
        content = f.read().lower()
        assert "create " in content and "index " in content, f"{sql_path} does not contain CREATE INDEX statements."

    db_path = "/home/user/store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if custom indexes exist in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No custom indexes found in the database. Ensure indexes.sql was executed."

    conn.close()

def test_top_spenders_csv():
    csv_path = "/home/user/top_spenders.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = list(csv.reader(f))

    assert len(reader) == 4, f"Expected exactly 1 header row and 3 data rows in {csv_path}, found {len(reader)}."

    headers = reader[0]
    assert headers == ["client_name", "total_spent"], f"Incorrect headers. Expected ['client_name', 'total_spent'], got {headers}."

    # Parse results
    results = []
    for row in reader[1:]:
        assert len(row) == 2, f"Expected 2 columns per row, got {len(row)} in row {row}"
        client_name = row[0].strip()
        try:
            total_spent = float(row[1].strip())
        except ValueError:
            pytest.fail(f"Could not parse total_spent '{row[1]}' as float.")
        results.append((client_name, total_spent))

    # Expected data: Alice Smith (1200), Charlie Brown (1200), Bob Jones (200)
    # The order of Alice and Charlie can vary, but Bob must be last.
    top_two = sorted([results[0], results[1]])
    expected_top_two = sorted([("Alice Smith", 1200.0), ("Charlie Brown", 1200.0)])

    assert top_two == expected_top_two, f"Expected top two spenders to be Alice Smith and Charlie Brown with 1200.0, got {top_two}."
    assert results[2] == ("Bob Jones", 200.0), f"Expected third spender to be Bob Jones with 200.0, got {results[2]}."

def test_query_sql_exists():
    sql_path = "/home/user/query.sql"
    assert os.path.isfile(sql_path), f"File {sql_path} does not exist."
    with open(sql_path, 'r') as f:
        content = f.read().lower()
        assert "select" in content, f"{sql_path} does not appear to contain a valid SQL SELECT query."