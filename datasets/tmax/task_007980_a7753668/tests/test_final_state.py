# test_final_state.py

import os
import sqlite3

PROJECT_DIR = "/home/user/project"
OUTPUT_LOG = os.path.join(PROJECT_DIR, "output.log")
DB_PATH = os.path.join(PROJECT_DIR, "db.sqlite")

def test_output_log_exists_and_correct():
    assert os.path.isfile(OUTPUT_LOG), f"Expected output log at {OUTPUT_LOG} was not found. Did the application run successfully?"

    with open(OUTPUT_LOG, "r") as f:
        content = f.read().strip()

    expected_content = "System OK. Name: PolyglotGraphSystem, Version: 2"
    assert content == expected_content, f"Output log content is incorrect.\nExpected: '{expected_content}'\nFound: '{content}'"

def test_database_migration_applied():
    assert os.path.isfile(DB_PATH), f"Database at {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT version FROM config LIMIT 1;")
        row = cursor.fetchone()
        assert row is not None, "No data found in the 'config' table."
        assert row[0] == 2, f"Expected version 2 in 'config' table, but found {row[0]}."
    except sqlite3.OperationalError as e:
        if "no such column: version" in str(e):
            assert False, "Migration was not applied: 'version' column is missing from 'config' table."
        else:
            raise
    finally:
        conn.close()

def test_rust_lib_fixed():
    lib_rs_path = os.path.join(PROJECT_DIR, "rust_lib/src/lib.rs")
    with open(lib_rs_path, "r") as f:
        content = f.read()
    assert "into_raw()" in content or "into_raw" in content, "The rust_lib does not appear to use `into_raw()` to fix the memory leak/borrow checker issue."

def test_cmake_fixed():
    cmake_path = os.path.join(PROJECT_DIR, "CMakeLists.txt")
    with open(cmake_path, "r") as f:
        content = f.read()
    assert "librust_lib.a" in content, "CMakeLists.txt does not link the compiled Rust library."
    assert "dl" in content and "pthread" in content and "m" in content, "CMakeLists.txt does not link the required system libraries (dl, pthread, m)."