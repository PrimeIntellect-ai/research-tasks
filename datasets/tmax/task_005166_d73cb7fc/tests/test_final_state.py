# test_final_state.py

import os
import re
import sqlite3
import subprocess
import pytest

REPORT_PATH = "/home/user/report.txt"
DB_PATH = "/home/user/data/metrics.db"
EXPECTED_COMMIT_FILE = "/tmp/expected_commit.txt"

def get_expected_commit():
    """Retrieve the expected commit hash from the setup truth file."""
    assert os.path.isfile(EXPECTED_COMMIT_FILE), f"Truth file {EXPECTED_COMMIT_FILE} is missing."
    with open(EXPECTED_COMMIT_FILE, "r") as f:
        return f.read().strip()

def get_expected_poison_id():
    """Derive the expected poison ID directly from the SQLite database."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM metrics")
    row = cursor.fetchone()
    conn.close()
    assert row is not None and row[0] is not None, "Could not find any metrics in the database."
    return str(row[0])

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_report_format_and_content():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    commit_match = re.search(r'Commit:\s*([a-f0-9]{40})', content, re.IGNORECASE)
    id_match = re.search(r'Poison ID:\s*(\d+)', content, re.IGNORECASE)

    assert commit_match is not None, "Report does not contain a valid 40-character Git commit hash in the format 'Commit: <hash>'."
    assert id_match is not None, "Report does not contain a valid Poison ID in the format 'Poison ID: <id>'."

    actual_commit = commit_match.group(1).lower()
    actual_id = id_match.group(1)

    expected_commit = get_expected_commit().lower()
    expected_id = get_expected_poison_id()

    assert actual_commit == expected_commit, f"Incorrect bad commit hash. Expected {expected_commit}, but got {actual_commit}."
    assert actual_id == expected_id, f"Incorrect Poison ID. Expected {expected_id}, but got {actual_id}."