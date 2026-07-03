# test_final_state.py

import os
import stat
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/backup_metadata.db"
GENERATE_SCRIPT = "/home/user/generate_report.sh"
OPTIMIZE_SCRIPT = "/home/user/optimize.sh"
REPORT_PATH = "/home/user/final_report.csv"

EXPECTED_CSV = [
    "cache-master,ROOT,210",
    "cache-node1,cache-master,190",
    "db-main,ROOT,1060",
    "db-replica1,db-main,955",
    "db-replica2,db-main,960"
]

def test_scripts_exist_and_executable():
    for script in [GENERATE_SCRIPT, OPTIMIZE_SCRIPT]:
        assert os.path.exists(script), f"Script missing at {script}"
        assert os.path.isfile(script), f"{script} is not a file"
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"{script} is not executable"

def test_generate_report_correctness():
    # Remove the report if it exists to ensure the script creates it
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Run the script
    result = subprocess.run([GENERATE_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{GENERATE_SCRIPT} failed to execute properly. Stderr: {result.stderr}"

    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} was not created by the script"

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(EXPECTED_CSV), f"Expected {len(EXPECTED_CSV)} rows in CSV, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, EXPECTED_CSV)):
        assert actual == expected, f"Row {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_optimize_script_creates_index():
    # Check if index exists, drop it if it does to test the script
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_backups_latest';")
    index_exists = cursor.fetchone() is not None

    if index_exists:
        cursor.execute("DROP INDEX idx_backups_latest;")
        conn.commit()

    conn.close()

    # Run the optimize script
    result = subprocess.run([OPTIMIZE_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{OPTIMIZE_SCRIPT} failed to execute properly. Stderr: {result.stderr}"

    # Verify the index was created
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_backups_latest';")
    assert cursor.fetchone() is not None, "Index 'idx_backups_latest' was not created by optimize.sh"

    # Verify the index is on the backups table
    cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='index' AND name='idx_backups_latest';")
    tbl_name = cursor.fetchone()[0]
    assert tbl_name == 'backups', f"Index 'idx_backups_latest' is on table '{tbl_name}', expected 'backups'"

    conn.close()