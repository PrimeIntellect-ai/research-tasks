# test_final_state.py

import os
import sqlite3
import pytest

WORKSPACE_DIR = "/home/user/pr_review"
SUCCESS_LOG = "/home/user/ci_success.log"

def test_ci_success_log_exists():
    assert os.path.isfile(SUCCESS_LOG), (
        f"The CI success log {SUCCESS_LOG} does not exist. "
        "Did you run ./run_ci.sh successfully?"
    )

def test_ci_success_log_content():
    with open(SUCCESS_LOG, "r") as f:
        content = f.read().strip()
    assert content == "CI PASS", (
        f"Expected {SUCCESS_LOG} to contain exactly 'CI PASS', but got '{content}'."
    )

def test_c_code_bounds_error_fixed():
    c_file = os.path.join(WORKSPACE_DIR, "math_engine.c")
    assert os.path.isfile(c_file), f"File {c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()

    # The bug was in the first loop: for(int i = 0; i <= len; i++)
    # It should be fixed to i < len.
    assert "i <= len" not in content, (
        "The off-by-one bounds error (i <= len) is still present in math_engine.c."
    )

def test_makefile_has_math_lib_linked():
    makefile_path = os.path.join(WORKSPACE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lm" in content, (
        "The Makefile is still missing the '-lm' flag required to link the math library."
    )

def test_schema_v2_has_alter_table():
    schema_v2_path = os.path.join(WORKSPACE_DIR, "schema_v2.sql")
    assert os.path.isfile(schema_v2_path), f"File {schema_v2_path} is missing."
    with open(schema_v2_path, "r") as f:
        content = f.read().upper()

    assert "ALTER TABLE" in content and "ADD" in content and "VARIANCE" in content, (
        "schema_v2.sql does not appear to contain a valid ALTER TABLE statement adding the variance column."
    )

def test_sqlite_database_schema():
    db_path = os.path.join(WORKSPACE_DIR, "test.db")
    assert os.path.isfile(db_path), (
        f"Database file {db_path} is missing. The CI script may have failed to run or complete."
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the stats table has the variance column
    cursor.execute("PRAGMA table_info(stats);")
    columns = cursor.fetchall()
    conn.close()

    col_names = [col[1] for col in columns]
    assert "variance" in col_names, (
        "The 'variance' column was not found in the 'stats' table. "
        "The schema migration failed or was incorrect."
    )