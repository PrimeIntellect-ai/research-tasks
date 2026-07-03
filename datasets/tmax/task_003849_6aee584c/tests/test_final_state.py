# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/datasets.db"
GO_SCRIPT_PATH = "/home/user/graph_query.go"
OUTPUT_PATH = "/home/user/top_consumers.txt"

def test_output_file_contents():
    """Verify that the output file contains the exactly correct top 3 consumers."""
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

    with open(OUTPUT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Clinical_Correlations",
        "GWAS_Summary",
        "Population_Frequencies"
    ]

    assert lines == expected_lines, f"Expected {expected_lines}, but got {lines}. The Go script did not produce the correct output."

def test_database_indexes():
    """Verify that appropriate indexes were created to optimize the queries."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()

    # We expect indexes on dependencies(target_id) and datasets(domain, size_mb) or similar
    # Let's check which tables have indexes
    indexed_tables = [idx[1] for idx in indexes]

    assert "dependencies" in indexed_tables, "No index was created on the 'dependencies' table to optimize graph traversal."
    assert "datasets" in indexed_tables, "No index was created on the 'datasets' table to optimize filtering/sorting."

    conn.close()

def test_go_script_exists_and_content():
    """Verify that the Go script exists and contains expected SQL and imports."""
    assert os.path.exists(GO_SCRIPT_PATH), f"Go script {GO_SCRIPT_PATH} does not exist."

    with open(GO_SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "database/sql" in content, "Go script does not import 'database/sql'."
    assert "github.com/mattn/go-sqlite3" in content, "Go script does not import the sqlite3 driver."
    assert "WITH RECURSIVE" in content.upper(), "Go script does not appear to use a Recursive CTE."
    assert "os.Args" in content or "flag." in content, "Go script does not appear to read command-line arguments."