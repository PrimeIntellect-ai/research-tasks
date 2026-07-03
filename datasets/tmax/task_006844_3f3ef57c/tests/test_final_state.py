# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/company.db"
RESULTS_PATH = "/home/user/results.json"

def test_database_exists():
    """Test that the SQLite database was created at the correct path."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} was not found."

def test_results_json_exists():
    """Test that the results.json file was created."""
    assert os.path.isfile(RESULTS_PATH), f"Results file {RESULTS_PATH} was not found."

def test_results_json_content():
    """Test that results.json contains the correct aggregated values."""
    with open(RESULTS_PATH, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_PATH} is not a valid JSON file.")

    assert "total_inter_dept_messages" in results, "Missing 'total_inter_dept_messages' in results.json"
    assert "top_dept_in_degree" in results, "Missing 'top_dept_in_degree' in results.json"
    assert "indexes_created" in results, "Missing 'indexes_created' in results.json"

    assert results["total_inter_dept_messages"] == 59, \
        f"Expected 59 total inter-department messages, got {results['total_inter_dept_messages']}"

    assert results["top_dept_in_degree"] == "HR", \
        f"Expected top department to be 'HR', got '{results['top_dept_in_degree']}'"

    assert isinstance(results["indexes_created"], list), "'indexes_created' should be a list"
    assert len(results["indexes_created"]) >= 2, \
        f"Expected at least 2 indexes created, found {len(results['indexes_created'])}"

def test_database_indexes_exist():
    """Test that the indexes specified in results.json actually exist in the database."""
    with open(RESULTS_PATH, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_PATH} is not a valid JSON file.")

    indexes_created = results.get("indexes_created", [])
    if not isinstance(indexes_created, list) or len(indexes_created) < 2:
        pytest.skip("indexes_created is not a valid list of at least 2 items; already caught by another test.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    db_indexes = [row[0] for row in cursor.fetchall()]
    conn.close()

    for idx in indexes_created:
        assert idx in db_indexes, f"Index '{idx}' reported in results.json was not found in {DB_PATH}"

def test_foreign_keys_enabled():
    """Test that foreign keys were used in the schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables for foreign key constraints
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    fk_found = False
    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()
        if fks:
            fk_found = True
            break

    conn.close()
    assert fk_found, "No foreign key constraints were found in the database schema."