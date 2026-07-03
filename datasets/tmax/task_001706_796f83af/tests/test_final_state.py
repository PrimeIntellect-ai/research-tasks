# test_final_state.py
import os
import sqlite3

def test_raw_logs_unmodified():
    filepath = "/home/user/app/raw_logs.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()

    expected_content = """10.0.1.15|2023-10-25T08:12:01Z|200|/index.html
10.0.1.22|2023-10-25T08:12:05Z|500|/api/checkout
10.0.1.33|2023-10-25T08:12:10Z|200|/images/logo.png
10.0.1.99|2023-10-25T08:12:15Z|200
10.0.1.45|2023-10-25T08:12:20Z|500|/api/login
10.0.1.50|2023-10-25T08:12:25Z|404|/favicon.ico
"""
    assert content == expected_content, "raw_logs.txt was modified, which violates the constraints."

def test_database_populated():
    db_path = "/home/user/app/db.sqlite"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing. Did you run the parser?"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM logs")
        count = cursor.fetchone()[0]
    except sqlite3.Error as e:
        conn.close()
        assert False, f"Failed to query the logs table: {e}"
    conn.close()

    assert count == 5, f"Expected 5 rows in the logs table, but found {count}. Did you skip the malformed line correctly?"

def test_forensics_report():
    report_path = "/home/user/forensics_report.txt"
    assert os.path.isfile(report_path), f"Forensics report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    assert len(lines) == 3, f"Forensics report should have exactly 3 lines, but found {len(lines)}."

    assert lines[0] == "10.0.1.99|2023-10-25T08:12:15Z|200", f"Line 1 of report is incorrect. Found: {lines[0]}"
    assert lines[1] == "5", f"Line 2 of report is incorrect. Expected '5', found: {lines[1]}"
    assert lines[2] == "10.0.1.22,10.0.1.45", f"Line 3 of report is incorrect. Found: {lines[2]}"

def test_analyzer_script_fixed():
    analyzer_path = "/home/user/app/analyzer.py"
    assert os.path.isfile(analyzer_path), f"Script {analyzer_path} is missing."

    with open(analyzer_path, "r") as f:
        content = f.read()

    assert "status = '500'" in content or 'status="500"' in content or "status=500" in content or "status = 500" in content, \
        "analyzer.py does not appear to query for status 500."