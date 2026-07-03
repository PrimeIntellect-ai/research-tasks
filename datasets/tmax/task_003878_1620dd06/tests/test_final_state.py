# test_final_state.py

import os
import sqlite3

def test_script_exists_and_executable():
    script_path = "/home/user/process_events.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_database_exists():
    db_path = "/home/user/analytics.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

def test_database_content():
    db_path = "/home/user/analytics.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events';")
    assert cursor.fetchone() is not None, "Table 'events' does not exist in the database."

    # Fetch all rows
    cursor.execute("SELECT id, timestamp, email, action, amount FROM events ORDER BY id ASC;")
    rows = cursor.fetchall()

    expected_rows = [
        (1, "2023-01-01 00:00:00", "***@example.com", "LOGIN", 0),
        (2, "2023-01-01 01:30:00", "***@domain.com", "PURCHASE", 50),
        (3, "2023-01-01 02:00:00", "***@test.org", "LOGOUT", 0),
        (4, "2023-01-02 10:15:00", "***@example.com", "PURCHASE", 120),
        (5, "2023-01-03 10:00:00", "***@hacker.net", "PURCHASE", 300)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

    for i, (row, expected) in enumerate(zip(rows, expected_rows)):
        assert row == expected, f"Row {i+1} mismatch. Expected {expected}, got {row}."

    conn.close()

def test_report_html_content():
    report_path = "/home/user/report.html"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = """<html>
<body>
<h1>Daily Report</h1>
<p>Total Events: 5</p>
<p>Unique Domains: 4</p>
<p>Total Revenue: $470</p>
</body>
</html>"""

    # Normalize newlines and spaces for robust comparison
    def normalize(text):
        return "\n".join([line.strip() for line in text.strip().splitlines() if line.strip()])

    assert normalize(content) == normalize(expected_content), "The content of report.html does not match the expected output."