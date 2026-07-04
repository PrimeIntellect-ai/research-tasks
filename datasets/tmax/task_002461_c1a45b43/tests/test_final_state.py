# test_final_state.py

import os
import sqlite3
import pytest

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Expected report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Targeted Service: sshd\nTotal Records: 8"
    assert content == expected_content, (
        f"Content of {report_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )

def test_database_records():
    db_path = "/home/user/stolen_data.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check total records
        cursor.execute("SELECT COUNT(*) FROM exfiltration_logs;")
        count = cursor.fetchone()[0]
        assert count == 8, f"Expected 8 records in exfiltration_logs table, but found {count}."

        # Check earliest timestamp
        cursor.execute("SELECT MIN(timestamp) FROM exfiltration_logs;")
        min_ts = cursor.fetchone()[0]
        assert min_ts == 1680000000, f"Expected minimum timestamp to be 1680000000, but found {min_ts}."

        # Ensure the 6th record (which was oversized) was properly truncated and inserted
        cursor.execute("SELECT data FROM exfiltration_logs WHERE timestamp = 1680000075;")
        oversized_data = cursor.fetchone()
        assert oversized_data is not None, "The oversized record was not found in the database."
        assert len(oversized_data[0]) <= 255, "The oversized record was not properly truncated to fit within 255 bytes."

    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query the database. Is the schema correct? Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()