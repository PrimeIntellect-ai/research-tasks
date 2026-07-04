# test_final_state.py

import os
import sqlite3
import pytest
import re

def test_output_edges_csv():
    file_path = "/home/user/output_edges.csv"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_edges = {
        "Alice,Alpha",
        "Bob,Alpha",
        "Bob,Beta",
        "Charlie,Beta"
    }

    assert set(lines) == expected_edges, f"Edges in {file_path} do not match the expected set. Found: {lines}"
    assert len(lines) == 4, f"{file_path} should contain exactly 4 edges, but found {len(lines)}."

def test_index_sql_file():
    file_path = "/home/user/index.sql"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().lower()

    assert "create " in content and "index " in content, f"{file_path} does not contain a CREATE INDEX statement."
    assert "employee_projects" in content, f"{file_path} does not reference the employee_projects table."
    assert "emp_id" in content and "proj_id" in content, f"{file_path} does not reference both emp_id and proj_id columns."

def test_index_applied_to_db():
    db_path = "/home/user/data.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('employee_projects');")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No index found on the employee_projects table in the database."

    valid_index_found = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = {row[2] for row in cursor.fetchall()}

        if columns == {"emp_id", "proj_id"}:
            valid_index_found = True
            break

    conn.close()

    assert valid_index_found, "No composite index covering both emp_id and proj_id was found on the employee_projects table."