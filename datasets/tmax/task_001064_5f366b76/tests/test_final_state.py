# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/backups.db"
BAD_INDEX_FILE = "/home/user/bad_index.txt"
ANALYZE_SCRIPT = "/home/user/analyze_graph.sh"
TOP_JOBS_FILE = "/home/user/top_jobs.csv"
BACKUP_PATHS_FILE = "/home/user/backup_paths.csv"

def test_bad_index_file():
    assert os.path.exists(BAD_INDEX_FILE), f"File {BAD_INDEX_FILE} is missing."
    with open(BAD_INDEX_FILE, "r") as f:
        content = f.read().strip()
    assert content == "idx_deps_child_only", f"Expected 'idx_deps_child_only' in {BAD_INDEX_FILE}, got '{content}'"

def test_database_indexes():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that bad index is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_deps_child_only';")
    assert cursor.fetchone() is None, "The bad index 'idx_deps_child_only' was not dropped."

    # Check that new optimal index exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_deps_optimal';")
    assert cursor.fetchone() is not None, "The optimal index 'idx_deps_optimal' was not created."

    # Check columns of the new index
    cursor.execute("PRAGMA index_info('idx_deps_optimal');")
    index_info = cursor.fetchall()
    columns = [row[2] for row in index_info]
    assert columns == ['parent_id', 'child_id'], f"Index 'idx_deps_optimal' should be on (parent_id, child_id), but got {columns}"

    conn.close()

def test_analyze_script_executable():
    assert os.path.exists(ANALYZE_SCRIPT), f"Script {ANALYZE_SCRIPT} is missing."
    assert os.access(ANALYZE_SCRIPT, os.X_OK), f"Script {ANALYZE_SCRIPT} is not executable."

def test_top_jobs_csv():
    assert os.path.exists(TOP_JOBS_FILE), f"File {TOP_JOBS_FILE} is missing."
    with open(TOP_JOBS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,SystemDB,2",
        "1,AppDB,2",
        "3,UserDB,1"
    ]

    assert sorted(lines) == sorted(expected_lines), f"Expected {expected_lines} in {TOP_JOBS_FILE}, got {lines}"

def test_backup_paths_csv():
    assert os.path.exists(BACKUP_PATHS_FILE), f"File {BACKUP_PATHS_FILE} is missing."
    with open(BACKUP_PATHS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "SystemDB",
        "SystemDB->AppDB",
        "SystemDB->LogDB",
        "SystemDB->AppDB->UserDB",
        "SystemDB->AppDB->PaymentDB",
        "SystemDB->AppDB->UserDB->AnalyticsDB"
    ]

    assert sorted(lines) == sorted(expected_lines), f"Expected {expected_lines} in {BACKUP_PATHS_FILE}, got {lines}"