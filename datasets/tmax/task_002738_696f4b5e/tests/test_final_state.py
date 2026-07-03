# test_final_state.py

import os
import sqlite3
import pytest

def test_recovered_database_exists_and_valid():
    recovered_db_path = "/home/user/recovered_metrics.db"
    assert os.path.isfile(recovered_db_path), f"Recovered database file {recovered_db_path} is missing."

    # Check if it's a valid SQLite database by checking the header
    with open(recovered_db_path, "rb") as f:
        header = f.read(16)
    assert header == b"SQLite format 3\x00", f"File {recovered_db_path} is not a valid SQLite database."

    # Verify that we can query it and the data is intact
    try:
        conn = sqlite3.connect(recovered_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT latency FROM requests ORDER BY latency ASC")
        rows = cursor.fetchall()
        latencies = [row[0] for row in rows]
        assert latencies == [1000000001.0, 1000000002.0, 1000000003.0, 1000000004.0, 1000000005.0], "Recovered database does not contain the correct data."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to read from recovered database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_script_updated():
    script_path = "/home/user/calc_metrics.sh"
    assert os.path.isfile(script_path), f"Script file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "/home/user/recovered_metrics.db" in content, "Script was not updated to use the recovered database."

def test_variance_report_correct():
    report_path = "/home/user/variance_report.txt"
    assert os.path.isfile(report_path), f"Variance report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "2.50", f"Variance report contains '{content}', expected exactly '2.50'."