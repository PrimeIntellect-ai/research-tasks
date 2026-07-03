# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_database_created_and_populated():
    db_path = "/home/user/app/test.db"
    assert os.path.isfile(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_meta'")
    assert cursor.fetchone() is not None, "Table 'file_meta' does not exist in the database."

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='checksum_data'")
    assert cursor.fetchone() is not None, "Table 'checksum_data' does not exist in the database."

    # Check data inserted
    cursor.execute("SELECT count(*) FROM file_meta")
    file_meta_count = cursor.fetchone()[0]
    assert file_meta_count >= 1, "Expected at least 1 row in 'file_meta' table."

    cursor.execute("SELECT count(*) FROM checksum_data")
    checksum_data_count = cursor.fetchone()[0]
    assert checksum_data_count >= 1, "Expected at least 1 row in 'checksum_data' table."

    conn.close()

def test_shared_library_compiled():
    so_path = "/home/user/app/libecc/libecc.so"
    assert os.path.isfile(so_path), f"Shared library not found at {so_path}. Did you compile it?"

def test_qa_report_json():
    report_path = "/home/user/app/qa_report.json"
    assert os.path.isfile(report_path), f"QA report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {report_path} is not valid JSON.")

    assert "db_created" in data, "Key 'db_created' missing from QA report."
    assert data["db_created"] is True, "Expected 'db_created' to be true."

    assert "payload_checksum" in data, "Key 'payload_checksum' missing from QA report."
    expected_checksum = ("A" * 100) + "1234"
    assert data["payload_checksum"] == expected_checksum, (
        f"Expected payload_checksum to be 100 'A's followed by '1234', "
        f"but got '{data['payload_checksum']}'"
    )

def test_c_extension_fixed():
    c_file_path = "/home/user/app/libecc/ecc.c"
    assert os.path.isfile(c_file_path), f"C file not found at {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    # The original had malloc(len + 1). It should be changed to allocate enough space for "1234" (4 chars + null terminator = 5)
    assert "malloc(len + 1)" not in content, "The memory allocation bug in ecc.c has not been fixed (still using malloc(len + 1))."