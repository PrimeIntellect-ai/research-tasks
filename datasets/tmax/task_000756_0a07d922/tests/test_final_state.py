# test_final_state.py

import os
import sqlite3
import subprocess

def test_debugging_report_exists():
    report_path = "/home/user/debugging_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

def test_debugging_report_content():
    report_path = "/home/user/debugging_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    assert len(lines) >= 3, f"Expected at least 3 lines in {report_path}, found {len(lines)}."

    # Derive expected commit hash
    repo_path = "/home/user/uptime_monitor"
    result = subprocess.run(
        ["git", "log", "--grep=Update query logic", "--format=%H"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git log to find the regression commit."
    expected_commit = result.stdout.strip()
    assert expected_commit, "Could not find the regression commit in git history."

    # Derive expected uptime from the database
    db_path = "/home/user/logs.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ping_results WHERE status='UP';")
    up_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ping_results;")
    total_count = cursor.fetchone()[0]
    conn.close()

    expected_uptime_str = f"Uptime: {(up_count * 100.0) / total_count:.2f}%"
    expected_query = "SELECT COUNT(*) FROM ping_results WHERE status='UP';"

    assert lines[0] == expected_commit, f"Line 1 incorrect. Expected commit hash {expected_commit}, got {lines[0]}."
    assert lines[1] == expected_query, f"Line 2 incorrect. Expected '{expected_query}', got '{lines[1]}'."
    assert lines[2] == expected_uptime_str, f"Line 3 incorrect. Expected '{expected_uptime_str}', got '{lines[2]}'."