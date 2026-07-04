# test_final_state.py

import os
import sqlite3
import pytest

def test_init_db_script_exists_and_executable():
    script_path = "/home/user/init_db.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_analyze_provenance_script_exists_and_executable():
    script_path = "/home/user/analyze_provenance.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_database_exists_and_has_tables():
    db_path = "/home/user/provenance.db"
    assert os.path.isfile(db_path), f"Database missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert "datasets" in tables, "Table 'datasets' missing in database."
    assert "derivations" in tables, "Table 'derivations' missing in database."

    # Check indexes on derivations table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='derivations';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on 'derivations' table. Expected optimal indexes for graph traversal."

    conn.close()

def test_provenance_summary_csv():
    csv_path = "/home/user/provenance_summary.csv"
    assert os.path.isfile(csv_path), f"Output file missing: {csv_path}"

    expected_content = (
        "depth,total_size_mb,avg_processing_time\n"
        "0,100,0.0\n"
        "1,350,12.5\n"
        "2,700,17.5\n"
        "3,250,25.0"
    )

    with open(csv_path, "r") as f:
        actual_content = f.read().strip().replace('\r\n', '\n')

    assert actual_content == expected_content, (
        f"Content of {csv_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )