# test_final_state.py

import os
import sqlite3
import subprocess
import re
import pytest

def test_build_script_parallel_execution_maintained():
    path = "/home/user/project/build.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "&" in content, "The parallel execution feature (&) was removed from build.sh."

def test_database_all_done():
    db_path = "/home/user/project/build_state.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM tasks WHERE status='pending';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 0, f"Expected 0 pending tasks in the database, found {count}."

def test_fix_report_content():
    report_path = "/home/user/fix_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert re.search(r"ERROR=.*database is locked.*", content, re.IGNORECASE), \
        f"The report file does not contain the expected error message. Content: {content}"

def test_build_script_execution():
    init_script = "/home/user/project/init_db.sh"
    build_script = "/home/user/project/build.sh"

    # Re-initialize the database to ensure we start from a clean state
    subprocess.run([init_script], check=True)

    # Run the build script
    result = subprocess.run([build_script], capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check DB again to ensure the script actually fixed the issue
    db_path = "/home/user/project/build_state.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM tasks WHERE status='pending';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 0, f"After running build.sh, expected 0 pending tasks, found {count}."