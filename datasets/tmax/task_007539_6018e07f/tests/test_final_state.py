# test_final_state.py

import os
import sqlite3
import pytest

def test_files_exist_and_executable():
    scripts = [
        "/home/user/migrate.sh",
        "/home/user/build_and_run.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Expected script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

    assert os.path.isfile("/home/user/custom.s"), "Assembly file /home/user/custom.s does not exist."
    assert os.path.isfile("/home/user/legacy/libcustom.so"), "Shared library /home/user/legacy/libcustom.so was not created."

def test_database_schema_updated():
    db_path = "/home/user/legacy/db.sqlite"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(metrics);")
    columns = {row[1] for row in cursor.fetchall()}

    assert "hash_val" in columns, "Column 'hash_val' was not added to the 'metrics' table."

    conn.close()

def test_database_contents_updated():
    db_path = "/home/user/legacy/db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, raw_val, hash_val FROM metrics ORDER BY id;")
    rows = cursor.fetchall()

    expected_rows = []
    for row in [(1, 100), (2, 255), (3, 0)]:
        raw_val = row[1]
        hash_val = (raw_val ^ 0x5A) + 12
        expected_rows.append((row[0], raw_val, hash_val))

    assert rows == expected_rows, f"Database contents do not match expected values. Got {rows}, expected {expected_rows}."

    conn.close()

def test_final_dump_txt_contents():
    dump_path = "/home/user/final_dump.txt"
    assert os.path.isfile(dump_path), f"Dump file {dump_path} does not exist."

    with open(dump_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = []
    for row in [(1, 100), (2, 255), (3, 0)]:
        raw_val = row[1]
        hash_val = (raw_val ^ 0x5A) + 12
        expected_lines.append(f"{row[0]}|{raw_val}|{hash_val}")

    assert lines == expected_lines, f"Contents of {dump_path} do not match expected values. Got {lines}, expected {expected_lines}."