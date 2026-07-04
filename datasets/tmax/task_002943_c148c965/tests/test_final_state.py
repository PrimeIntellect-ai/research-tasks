# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/papers.db"
CSV_PATH = "/home/user/citation_summary.csv"

def test_database_index_created():
    """Check if the required index was created on the citations table."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('citations')")
    indexes = cursor.fetchall()

    valid_index_found = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}')")
        columns = [row[2] for row in cursor.fetchall()]
        # The index should start with cited_id to optimize bottom-up queries
        if columns and columns[0] == 'cited_id':
            valid_index_found = True
            break

    conn.close()
    assert valid_index_found, "Required index on 'citations' table (starting with 'cited_id') was not found."

def test_csv_output():
    """Check if the CSV output matches the expected aggregation."""
    assert os.path.exists(CSV_PATH), f"CSV file missing at {CSV_PATH}"

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = """depth,domain,count
1,Biology,3
1,Computer Science,2
1,Mathematics,2
1,Physics,3
2,Biology,7
2,Computer Science,8
2,Mathematics,7
2,Physics,8
3,Biology,12
3,Computer Science,13
3,Mathematics,12
3,Physics,13"""

    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, (
        f"CSV content does not match the expected output.\n"
        f"Expected {len(expected_lines)} lines, got {len(content_lines)} lines.\n"
        f"Expected:\n{expected_content}\nGot:\n{content}"
    )