# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_stale_edges_file():
    txt_path = "/home/user/stale_edges.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    # The initial DB has ids 1,2,3,4,5 and truth has 1,2,4. Stale are 3, 5.
    expected_stale = ["3", "5"]
    assert lines == expected_stale, f"Expected stale_edges.txt to contain exactly {expected_stale}, but got {lines}."

def test_optimize_sql_and_db_state():
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"File {sql_path} does not exist."

    with open(sql_path, "r") as f:
        sql_script = f.read()

    db_path = "/home/user/data/graph.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the script to apply changes (if not already applied by the student)
    try:
        cursor.executescript(sql_script)
        conn.commit()
    except sqlite3.OperationalError as e:
        # Ignore error if the index already exists (meaning the student ran the script themselves)
        if "already exists" not in str(e).lower():
            pytest.fail(f"Failed to execute optimize.sql: {e}")

    # Check rows remaining in the edges table
    cursor.execute("SELECT id, source, target FROM edges ORDER BY id;")
    rows = cursor.fetchall()

    json_path = "/home/user/data/truth_edges.json"
    with open(json_path, "r") as f:
        truth_data = json.load(f)

    expected_rows = [(item["id"], item["source"], item["target"]) for item in truth_data]
    expected_rows.sort(key=lambda x: x[0])

    assert rows == expected_rows, f"Edges table does not match truth data after applying optimize.sql. Expected {expected_rows}, got {rows}."

    # Check if the index exists and is on the correct columns
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_edges_src_tgt';")
    index_count = cursor.fetchone()[0]
    assert index_count == 1, "Index 'idx_edges_src_tgt' does not exist in the database."

    cursor.execute("PRAGMA index_info('idx_edges_src_tgt');")
    index_info = cursor.fetchall()

    # PRAGMA index_info returns rows like: (seqno, cid, name)
    # We need to ensure it covers 'source' then 'target'
    assert len(index_info) == 2, f"Index 'idx_edges_src_tgt' should cover exactly 2 columns, got {len(index_info)}."

    index_columns = [info[2] for info in index_info]
    assert index_columns == ["source", "target"], f"Index 'idx_edges_src_tgt' should be on columns ('source', 'target'), but got {tuple(index_columns)}."

    conn.close()