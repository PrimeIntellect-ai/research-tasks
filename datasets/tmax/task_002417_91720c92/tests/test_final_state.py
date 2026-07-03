# test_final_state.py
import os
import sqlite3
import pytest

def test_result_log():
    log_path = "/home/user/waf_project/result.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. The application may not have been run or output was not redirected."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Decoded: SELECT * FROM users"
    assert expected in content, f"Expected '{expected}' in {log_path}, but got: {content}"

def test_database_schema():
    db_path = "/home/user/waf_project/rules.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(rules);")
    columns = cursor.fetchall()

    col_names = [col[1] for col in columns]
    assert "action" in col_names, "The 'action' column is missing from the 'rules' table schema."

    # Check default value
    action_col = next((col for col in columns if col[1] == "action"), None)
    assert action_col is not None
    # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
    # dflt_value is at index 4
    dflt_value = action_col[4]
    assert dflt_value in ("'block'", '"block"', "block"), f"Expected default value 'block' for action column, got {dflt_value}"

    conn.close()

def test_rust_binary_exists():
    debug_bin = "/home/user/waf_project/rust_app/target/debug/waf_app"
    release_bin = "/home/user/waf_project/rust_app/target/release/waf_app"

    assert os.path.isfile(debug_bin) or os.path.isfile(release_bin), "Rust binary 'waf_app' not found in target/debug/ or target/release/. Did the build succeed?"

def test_c_shared_library_exists():
    so_path = "/home/user/waf_project/c_src/libparser.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} is missing. Did the C code compile successfully?"