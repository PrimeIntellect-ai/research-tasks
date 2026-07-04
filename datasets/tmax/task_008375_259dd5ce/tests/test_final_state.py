# test_final_state.py
import os
import sqlite3
import pytest

def test_c_files_exist():
    assert os.path.isfile("/home/user/audit.c"), "/home/user/audit.c does not exist."
    assert os.path.isfile("/home/user/audit"), "/home/user/audit executable does not exist."
    assert os.access("/home/user/audit", os.X_OK), "/home/user/audit is not executable."

def test_index_created():
    db_path = "/home/user/corporate.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='events';")
    indexes = cursor.fetchall()
    conn.close()

    # Filter out auto-generated indexes which have NULL sql
    user_indexes = [idx for idx in indexes if idx[1] is not None]
    assert len(user_indexes) > 0, "No custom index found on the 'events' table. Query optimization step missed."

    # Verify the index involves the event_data column
    index_sql = user_indexes[0][1].lower()
    assert "event_data" in index_sql, "The created index does not appear to be an expression-based index on the 'event_data' column."

def test_csv_output():
    output_path = "/home/user/flagged_audits.csv"
    expected_path = "/tmp/expected_flagged_audits.csv"

    assert os.path.isfile(output_path), f"Output file {output_path} was not generated."
    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."

    with open(output_path, "r") as f:
        output_content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    with open(expected_path, "r") as f:
        expected_content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert output_content == expected_content, f"The contents of {output_path} do not match the expected output. Ensure data aggregation, filtering, and window functions are correctly applied."