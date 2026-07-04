# test_final_state.py

import os
import sqlite3

def test_kg_analyzer_script_exists():
    """Test that the kg_analyzer.py script exists."""
    assert os.path.isfile('/home/user/kg_analyzer.py'), "/home/user/kg_analyzer.py does not exist."

def test_sqlite_db_exists_and_schema():
    """Test that the kg.db database exists, has nodes/edges tables, and contains indexes."""
    db_path = '/home/user/kg.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for nodes and edges tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert 'nodes' in tables, "The 'nodes' table is missing from the database."
    assert 'edges' in tables, "The 'edges' table is missing from the database."

    # Check for indexes
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No custom indexes found in the database. An index strategy is required."

    # Check that at least one index is on the edges or nodes table
    indexed_tables = {row[1] for row in indexes}
    assert 'edges' in indexed_tables or 'nodes' in indexed_tables, "No indexes found on the 'edges' or 'nodes' tables."

    conn.close()

def test_treatment_candidates_output():
    """Test that the treatment_candidates.txt file exists and contains the correct output."""
    output_path = '/home/user/treatment_candidates.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_drugs = ['Albuterol', 'Fluticasone', 'Omalizumab']

    assert lines == expected_drugs, f"Expected output {expected_drugs}, but got {lines}."