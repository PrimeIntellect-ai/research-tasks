# test_final_state.py

import os
import sqlite3
import pytest

def test_optimize_sql_exists():
    sql_file = "/home/user/optimize.sql"
    assert os.path.isfile(sql_file), f"Optimization script {sql_file} does not exist."

def test_index_created():
    db_path = "/home/user/company.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_manager';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1, "Index 'idx_manager' was not created in the database."

def test_c_file_fixed():
    c_file_path = "/home/user/export_hierarchy.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} does not exist."

    with open(c_file_path, 'r') as f:
        content = f.read()

    assert "sqlite3_bind_int" in content, "The C program does not use 'sqlite3_bind_int' for parameter binding."

    # Check for some join condition logic
    assert "manager_id" in content and "id" in content and "=" in content, \
        "The recursive CTE does not appear to have a join condition (e.g., e.manager_id = s.id)."

def test_executable_exists():
    exe_path = "/home/user/export_hierarchy"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_reports_csv_content():
    csv_path = "/home/user/reports_1.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "1,Alice",
        "2,Bob",
        "3,Charlie",
        "4,David",
        "5,Eve",
        "6,Frank",
        "7,Grace"
    ]

    assert sorted(lines) == sorted(expected_lines), \
        f"The contents of {csv_path} do not match the expected recursive hierarchy for employee 1."