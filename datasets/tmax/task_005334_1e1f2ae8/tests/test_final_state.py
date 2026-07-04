# test_final_state.py

import os
import re
import sqlite3
import pytest

TICKET_DIR = "/home/user/ticket_402"
PARSER_C = os.path.join(TICKET_DIR, "parser.c")
FINAL_RESULT = os.path.join(TICKET_DIR, "final_result.txt")
COMPANY_DB = os.path.join(TICKET_DIR, "company.db")
RECOVERED_SQL = os.path.join(TICKET_DIR, "recovered_query.sql")

def test_parser_c_fixed_loop_counter():
    """Verify the loop counter bug in parser.c is fixed."""
    assert os.path.isfile(PARSER_C), f"{PARSER_C} is missing."
    with open(PARSER_C, "r") as f:
        content = f.read()

    # Check that uint8_t i; is no longer used for the loop counter
    # The original had exactly `uint8_t i;`
    assert "uint8_t i;" not in content, "The loop counter 'i' is still declared as uint8_t, which causes an infinite loop."

def test_parser_c_has_assertion():
    """Verify the assertion for data_len < 10000 is added to parser.c."""
    assert os.path.isfile(PARSER_C), f"{PARSER_C} is missing."
    with open(PARSER_C, "r") as f:
        content = f.read()

    # Look for assert with data_len < 10000 or similar
    # Remove whitespace for easier matching
    stripped_content = re.sub(r'\s+', '', content)
    assert "assert(data_len<10000)" in stripped_content or "assert(10000>data_len)" in stripped_content, \
        "The required assertion `assert(data_len < 10000);` was not found in parser.c."

def test_final_result_exists_and_correct():
    """Verify final_result.txt contains the correct output."""
    assert os.path.isfile(FINAL_RESULT), f"{FINAL_RESULT} is missing."

    # Compute the expected output directly from the database
    assert os.path.isfile(COMPANY_DB), f"{COMPANY_DB} is missing."
    conn = sqlite3.connect(COMPANY_DB)
    c = conn.cursor()
    c.execute("SELECT username FROM employees WHERE role = 'admin' AND is_deleted = 1;")
    expected_rows = [row[0] for row in c.fetchall()]
    conn.close()

    with open(FINAL_RESULT, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert set(actual_lines) == set(expected_rows), \
        f"The contents of {FINAL_RESULT} do not match the expected query results. " \
        f"Expected: {expected_rows}, but got: {actual_lines}"

def test_recovered_sql_contains_is_deleted_filter():
    """Verify that the recovered SQL query was modified to filter by is_deleted = 1."""
    if os.path.isfile(RECOVERED_SQL):
        with open(RECOVERED_SQL, "r") as f:
            content = f.read().lower()
        assert "is_deleted" in content and "1" in content, \
            "The recovered_query.sql does not seem to contain the filter for is_deleted = 1."