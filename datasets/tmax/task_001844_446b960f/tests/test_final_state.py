# test_final_state.py

import os
import sqlite3
import pytest

def test_security_test_log_exists_and_correct():
    log_path = "/home/user/security_test.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you redirect the output of test_auth.sh?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "LOGIN_SUCCESS" in content, "Log file missing LOGIN_SUCCESS for valid login. The valid login attempt failed."
    assert "LOGIN_FAILED" in content, "Log file missing LOGIN_FAILED for SQL injection attempt. The injection attempt succeeded or wasn't handled properly."

def test_db_schema_updated():
    db_path = "/home/user/auth_service/db.sqlite"
    assert os.path.isfile(db_path), f"{db_path} is missing"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    conn.close()

    # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
    role_col = None
    for col in columns:
        if col[1] == "role":
            role_col = col
            break

    assert role_col is not None, "Column 'role' missing in users table. The schema migration was not applied."
    assert role_col[2].upper() == "TEXT", f"Column 'role' must be of type TEXT, but got {role_col[2]}"
    assert role_col[4] == "'user'", f"Column 'role' default value should be 'user', got {role_col[4]}"

def test_auth_api_fixed_with_parameterized_queries():
    cpp_path = "/home/user/auth_service/auth_api.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "sqlite3_bind_text" in content, "auth_api.cpp does not contain sqlite3_bind_text. Parameterized queries were not implemented."

def test_binary_built():
    bin_path = "/home/user/auth_service/auth_api"
    assert os.path.isfile(bin_path), f"{bin_path} is missing. Did you run make?"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."