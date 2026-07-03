# test_final_state.py

import os
import sqlite3
import pytest

def test_payload_extracted_correctly():
    payload_path = "/home/user/payload.bin"
    assert os.path.isfile(payload_path), f"Missing file: {payload_path}"

    with open(payload_path, "rb") as f:
        data = f.read()

    expected_data = b'\xff\x01\x02\x03'
    assert data == expected_data, f"Payload data is incorrect. Expected {expected_data}, got {data}"

def test_recovered_db_exists_and_valid():
    db_path = "/home/user/recovered.db"
    assert os.path.isfile(db_path), f"Missing file: {db_path}. The Rust tool was not run successfully."

    # Check if it's a valid SQLite database and contains the secrets table
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT recovery_key FROM secrets")
        row = cursor.fetchone()
        assert row is not None, "The 'secrets' table is empty or missing the expected row."
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to read from recovered SQLite database: {e}")

def test_flag_extracted_correctly():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Missing file: {flag_path}"

    with open(flag_path, "r") as f:
        flag_content = f.read().strip()

    expected_flag = "FLAG_RUST_GDB_RECOVERY_9921"
    assert flag_content == expected_flag, f"Flag content is incorrect. Expected {expected_flag}, got {flag_content}"

def test_parser_rs_fixed():
    parser_path = "/home/user/db_recovery/src/parser.rs"
    assert os.path.isfile(parser_path), f"Missing file: {parser_path}"

    with open(parser_path, "r") as f:
        content = f.read()

    # The original bug uses unsafe { std::ptr::copy_nonoverlapping(...) } without checking bounds.
    # The fix should either avoid unsafe entirely or add bounds checking.
    # We will verify that the original buggy line is no longer present in its exact form,
    # or that the file has been modified from the initial state.
    original_buggy_line = "std::ptr::copy_nonoverlapping(data.as_ptr().add(1), out.as_mut_ptr(), len);"
    assert original_buggy_line not in content or "len > data.len()" in content or "min" in content, \
        "The parser.rs file does not appear to be fixed. The original unsafe bug is still present without bounds checks."