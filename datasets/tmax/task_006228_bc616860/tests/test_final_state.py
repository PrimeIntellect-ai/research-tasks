# test_final_state.py

import os
import sqlite3
import stat
import re

def test_python_script_exists():
    assert os.path.isfile("/home/user/clean_data.py"), "/home/user/clean_data.py does not exist."

def test_bash_wrapper_exists_and_executable():
    path = "/home/user/run_job.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_cron_schedule_correct():
    path = "/home/user/schedule.cron"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    # Check for valid cron entry: 30 2 * * * /home/user/run_job.sh
    # We'll use a regex to allow multiple spaces or tabs
    pattern = r"30\s+2\s+\*\s+\*\s+\*\s+/home/user/run_job\.sh"
    assert re.search(pattern, content), f"{path} does not contain the correct cron schedule for 2:30 AM."

def test_database_contents():
    db_path = "/home/user/cleaned_data.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback';")
    assert cursor.fetchone() is not None, "Table 'feedback' does not exist in the database."

    # Check rows
    cursor.execute("SELECT id FROM feedback ORDER BY id;")
    rows = cursor.fetchall()
    ids = [row[0] for row in rows]
    expected_ids = ["101", "102", "201", "203", "302"]

    assert ids == expected_ids, f"Database does not contain the expected rows. Found IDs: {ids}"

    conn.close()

def test_error_log_contents():
    log_path = "/home/user/pipeline_errors.log"
    assert os.path.isfile(log_path), f"Error log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in error log, found {len(lines)}."

    expected_line1 = '[data2.jsonl] Line 2: {"id": "202", "user": "diana", "text": "Broken unicode \\u28ZZ here."}'
    expected_line2 = '[data3.jsonl] Line 1: {"id": "301", "user": "frank", "text": "Missing escape \\u1"}'

    assert expected_line1 in lines, f"Missing expected error log entry for data2.jsonl."
    assert expected_line2 in lines, f"Missing expected error log entry for data3.jsonl."