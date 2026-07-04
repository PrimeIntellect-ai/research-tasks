# test_final_state.py

import os
import sqlite3
import pytest

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read().strip()
    assert content == "3", f"Expected report.txt to contain '3', but got '{content}'."

def test_database_state():
    db_path = "/home/user/app/db.sqlite3"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        assert user_count == 3, f"Expected 3 users remaining in the database, found {user_count}."

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_info'")
        assert c.fetchone() is not None, "Table 'schema_info' does not exist."

        c.execute("SELECT version FROM schema_info")
        version_row = c.fetchone()
        assert version_row is not None, "Table 'schema_info' is empty."
        assert version_row[0] == 2, f"Expected schema version 2, got {version_row[0]}."
    finally:
        conn.close()

def test_test_migrate_file():
    test_file_path = "/home/user/app/tests/test_migrate.py"
    assert os.path.exists(test_file_path), f"Test file {test_file_path} does not exist."
    with open(test_file_path, "r") as f:
        content = f.read()
    assert "patch" in content or "Mock" in content, "The test file does not appear to use mocking (patch/Mock not found)."

def test_requirements_file():
    req_path = "/home/user/app/requirements.txt"
    assert os.path.exists(req_path), f"Requirements file {req_path} does not exist."
    with open(req_path, "r") as f:
        content = f.read()
    assert "pytest" in content, "pytest is missing from requirements.txt."
    assert "packaging" in content, "packaging is missing from requirements.txt."

def test_project_structure():
    assert os.path.isdir("/home/user/app/src"), "Directory /home/user/app/src does not exist."
    assert os.path.isdir("/home/user/app/tests"), "Directory /home/user/app/tests does not exist."
    assert os.path.isfile("/home/user/app/src/data_reader.py"), "File /home/user/app/src/data_reader.py does not exist."
    assert os.path.isfile("/home/user/app/src/migrate.py"), "File /home/user/app/src/migrate.py does not exist."