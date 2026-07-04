# test_final_state.py

import os
import sqlite3
import pytest

def test_metrics_recovered_db():
    db_path = "/home/user/metrics_recovered.db"
    assert os.path.isfile(db_path), f"Recovered database file {db_path} is missing."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        conn.close()
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered database is malformed or invalid: {e}")
    except sqlite3.OperationalError as e:
        pytest.fail(f"Could not query the 'events' table in recovered database: {e}")

    assert count == 5, f"Expected 5 rows in the 'events' table, but found {count}."

def test_check_db_script_exists():
    script_path = "/home/user/check_db.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

def test_diagnostic_report():
    report_path = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_path), f"Diagnostic report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected exactly 2 lines in diagnostic report, found {len(lines)}."
    assert lines[0] == "/home/user/legacy_plugin.so", f"First line of report is incorrect: {lines[0]}"
    assert lines[1] == "5", f"Second line of report is incorrect: {lines[1]}"