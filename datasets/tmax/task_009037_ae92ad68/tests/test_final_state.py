# test_final_state.py

import os
import sqlite3
import pytest

VIOLATIONS_FILE = '/home/user/violations.txt'
DB_PATH = '/home/user/audit.db'

def get_expected_violations():
    """
    Derive the expected violations directly from the database to ensure
    we are testing against the current state of the database.
    """
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = """
        SELECT DISTINCT u.id
        FROM t_usr u
        JOIN t_prm p ON u.id = p.usr_id
        JOIN t_ast a ON p.ast_id = a.id
        WHERE a.class = 'RESTRICTED'
          AND u.dept != a.owner_dept
          AND u.rl != 'AUDITOR'
        ORDER BY u.id ASC
    """

    c.execute(query)
    violations = [str(row[0]) for row in c.fetchall()]
    conn.close()

    return violations

def test_violations_file_exists():
    """Verify that the violations.txt file was created."""
    assert os.path.isfile(VIOLATIONS_FILE), f"The output file {VIOLATIONS_FILE} was not created."

def test_violations_content():
    """Verify that the violations.txt file contains the correct user IDs."""
    expected = get_expected_violations()

    with open(VIOLATIONS_FILE, 'r') as f:
        lines = f.read().splitlines()

    # Remove any empty lines
    actual = [line.strip() for line in lines if line.strip()]

    assert actual == expected, f"Expected violations {expected}, but found {actual} in {VIOLATIONS_FILE}."