# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/citations.db"
PATH_RESULT_FILE = "/home/user/path_result.txt"
CONCURRENCY_RESULT_FILE = "/home/user/concurrency_result.txt"
RUST_MAIN_FILE = "/home/user/dataset_manager/src/main.rs"

def test_path_result():
    assert os.path.isfile(PATH_RESULT_FILE), f"Expected result file {PATH_RESULT_FILE} does not exist."
    with open(PATH_RESULT_FILE, "r") as f:
        content = f.read().strip()

    # Compute the expected shortest path dynamically
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        WITH RECURSIVE path(id, depth) AS (
            SELECT 10, 0
            UNION ALL
            SELECT c.target_id, p.depth + 1
            FROM citations c
            JOIN path p ON c.source_id = p.id
            WHERE p.id != 42
        )
        SELECT min(depth) FROM path WHERE id = 42;
    """)
    row = cursor.fetchone()
    conn.close()

    expected_depth = str(row[0]) if row and row[0] is not None else "-1"
    assert content == expected_depth, f"Expected path length {expected_depth}, but got {content} in {PATH_RESULT_FILE}."

def test_concurrency_result():
    assert os.path.isfile(CONCURRENCY_RESULT_FILE), f"Expected result file {CONCURRENCY_RESULT_FILE} does not exist."
    with open(CONCURRENCY_RESULT_FILE, "r") as f:
        content = f.read().strip()
    assert "Concurrency test passed" in content, f"Expected 'Concurrency test passed' in {CONCURRENCY_RESULT_FILE}, got: {content}"

def test_sqlite_journal_mode():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0].lower()
    conn.close()
    assert mode == "wal", f"Expected SQLite journal mode to be 'wal', but it is '{mode}'."

def test_sqlite_index_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list('citations');")
    indexes = cursor.fetchall()

    found_idx = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = [col[2] for col in cursor.fetchall()]
        if columns == ['source_id', 'target_id'] or columns == ['target_id', 'source_id']:
            found_idx = True
            break

    conn.close()
    assert found_idx, "Expected an index on the 'citations' table for columns (source_id, target_id)."

def test_rust_code_modified():
    assert os.path.isfile(RUST_MAIN_FILE), f"Rust source file {RUST_MAIN_FILE} missing."
    with open(RUST_MAIN_FILE, "r") as f:
        content = f.read()

    assert "WITH RECURSIVE" in content.upper(), "Did not find 'WITH RECURSIVE' CTE in the Rust source code."
    assert "PRAGMA journal_mode" in content or "journal_mode=WAL" in content.upper() or "journal_mode = WAL" in content.upper(), "Did not find journal_mode configuration in the Rust source code."