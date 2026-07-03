# test_final_state.py

import os
import sqlite3
import pytest

VIOLATIONS_CSV = '/home/user/violations.csv'
DB_PATH = '/home/user/hierarchy.db'

def test_violations_csv_exists():
    assert os.path.exists(VIOLATIONS_CSV), f"Expected output file {VIOLATIONS_CSV} does not exist."
    assert os.path.isfile(VIOLATIONS_CSV), f"{VIOLATIONS_CSV} is not a file."

def test_violations_csv_contents():
    # Recalculate expected results to be robust
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = """
    WITH RECURSIVE descendants AS (
        SELECT id as root_id, id as node_id, local_size
        FROM nodes
        UNION ALL
        SELECT d.root_id, n.id, n.local_size
        FROM descendants d
        JOIN nodes n ON n.parent_id = d.node_id
    )
    SELECT n.id, n.name, SUM(d.local_size) as total_size, q.max_size
    FROM nodes n
    JOIN descendants d ON n.id = d.root_id
    JOIN quotas q ON n.id = q.node_id
    WHERE n.type = 'dir'
    GROUP BY n.id, n.name, q.max_size
    HAVING total_size > q.max_size
    ORDER BY n.id ASC;
    """
    c.execute(query)
    expected_rows = c.fetchall()
    conn.close()

    expected_csv_lines = [
        f"{row[0]},{row[1]},{row[2]},{row[3]}" for row in expected_rows
    ]

    with open(VIOLATIONS_CSV, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_csv_lines), \
        f"Expected {len(expected_csv_lines)} rows in CSV, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_csv_lines)):
        assert actual == expected, \
            f"Row {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"