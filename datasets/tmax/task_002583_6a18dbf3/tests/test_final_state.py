# test_final_state.py

import os
import sqlite3
import pytest

def test_report_exists_and_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"{report_path} was not created."

    with open(report_path, "r") as f:
        lines = f.read().strip().splitlines()

    # Remove all spaces and empty lines to be robust against formatting
    actual = [line.replace(" ", "") for line in lines if line.strip()]

    expected = [
        "Frank|Marketing|Alice|200|1",
        "Grace|Sales|Alice|400|1",
        "Eve|Sales|Alice|300|2",
        "David|Sales|Alice|250|3",
        "Charlie|Sales|Alice|50|4"
    ]

    assert actual == expected, f"Content of {report_path} does not match expected output."

def test_database_exists_and_has_indexes():
    db_path = "/home/user/company.db"
    assert os.path.isfile(db_path), f"Database file {db_path} was not created."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for indexes on employees or sales tables
    query = """
        SELECT count(*) FROM sqlite_master 
        WHERE type='index' AND (tbl_name='employees' OR tbl_name='sales')
    """
    try:
        cursor.execute(query)
        index_count = cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query sqlite_master in {db_path}: {e}")
    finally:
        conn.close()

    assert index_count >= 2, f"Expected at least 2 indexes on employees/sales tables, found {index_count}."