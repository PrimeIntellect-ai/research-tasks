# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/dag.db"
SCRIPT_PATH = "/home/user/analyze_graph.sh"
CRITICAL_PATH_TXT = "/home/user/critical_path.txt"
PLAN_TXT = "/home/user/plan.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "sqlite3" in content, "The script does not appear to invoke sqlite3."

def test_database_indexes():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='tasks'")
    indexes = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    assert "idx_parent" not in indexes, "The old corrupted index 'idx_parent' was not dropped."
    assert "idx_parent_id" in indexes, "The new index 'idx_parent_id' was not created."

    # Verify the index is actually on parent_id
    sql = indexes["idx_parent_id"].lower()
    assert "parent_id" in sql, f"The new index 'idx_parent_id' does not seem to index 'parent_id'. SQL: {sql}"

def test_critical_path_output():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    # Compute the expected critical path dynamically from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, parent_id, duration FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tree = {}
    durations = {}
    for tid, pid, dur in rows:
        durations[tid] = dur
        if pid not in tree:
            tree[pid] = []
        tree[pid].append(tid)

    def get_max_path(node):
        if node not in tree:
            return durations[node]
        return durations[node] + max(get_max_path(child) for child in tree[node])

    roots = tree.get(None, [])
    expected_max = max(get_max_path(r) for r in roots) if roots else 0

    assert os.path.isfile(CRITICAL_PATH_TXT), f"Output file {CRITICAL_PATH_TXT} does not exist."

    with open(CRITICAL_PATH_TXT, "r") as f:
        content = f.read().strip()

    expected_str = f"Critical Path Length: {expected_max}"
    assert content == expected_str, f"Expected '{expected_str}', but got '{content}'."

def test_query_plan_output():
    assert os.path.isfile(PLAN_TXT), f"Plan output file {PLAN_TXT} does not exist."

    with open(PLAN_TXT, "r") as f:
        content = f.read()

    assert "idx_parent_id" in content, "The EXPLAIN QUERY PLAN output in plan.txt does not reference the new index 'idx_parent_id'."