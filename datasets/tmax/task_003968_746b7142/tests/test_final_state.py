# test_final_state.py

import os
import sqlite3
import pytest

PROJECT_DIR = "/home/user/math_migrator"

def test_success_log_exists_and_correct():
    log_path = os.path.join(PROJECT_DIR, "success.log")
    assert os.path.isfile(log_path), f"success.log is missing at {log_path}."

    expected_lines = [
        "1|3 4 +|7",
        "2|5 6 * 2 +|32",
        "3|1 + + +|0",
        "4|7 8 *|56"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of success.log do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_database_schema_migrated():
    db_path = os.path.join(PROJECT_DIR, "data.db")
    assert os.path.isfile(db_path), f"Database data.db is missing at {db_path}."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(history);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert "id" in columns, "Column 'id' missing in 'history' table."
    assert "math_expr" in columns, "Column 'math_expr' missing in 'history' table (migration not applied?)."
    assert "result" in columns, "Column 'result' missing in 'history' table (migration not applied?)."
    assert "equation" not in columns, "Column 'equation' should have been renamed."

    conn.close()

def test_c_extension_migrated():
    c_path = os.path.join(PROJECT_DIR, "fastmath.c")
    assert os.path.isfile(c_path), f"fastmath.c is missing at {c_path}."

    with open(c_path, "r") as f:
        content = f.read()

    assert "Py_InitModule" not in content, "fastmath.c still contains Python 2 Py_InitModule."
    assert "PyModuleDef" in content or "PyModule_Create" in content, (
        "fastmath.c does not appear to use the Python 3 PyModuleDef / PyModule_Create API."
    )

def test_c_extension_safety_check():
    c_path = os.path.join(PROJECT_DIR, "fastmath.c")
    assert os.path.isfile(c_path), f"fastmath.c is missing at {c_path}."

    with open(c_path, "r") as f:
        content = f.read()

    # We check for some form of underflow check. 
    # The prompt explicitly mentions checking if sp < 2 or similar.
    # We will look for '2' and 'sp' in the same context or simply rely on the success.log result.
    # But let's also ensure the file has been modified to include some safety check.
    assert "< 2" in content or "<2" in content or "<= 1" in content or "<=1" in content, (
        "fastmath.c does not seem to contain an underflow check (e.g., checking if stack pointer < 2)."
    )