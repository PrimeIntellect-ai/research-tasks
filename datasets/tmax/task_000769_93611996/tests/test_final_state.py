# test_final_state.py
import os
import sqlite3
import time
import pytest

def test_database_and_data():
    db_path = '/home/user/network.db'
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topology'")
    assert cur.fetchone() is not None, "Table 'topology' does not exist in the database."

    cur.execute("SELECT parent_node, child_node FROM topology ORDER BY child_node")
    rows = cur.fetchall()

    # Re-derive expected edges based on the video generation logic (1000 frames, f % 3 == 0)
    expected_edges = []
    for f in range(1000):
        if f % 3 == 0:
            expected_edges.append(((f * 7) % 100, f))

    assert len(rows) == len(expected_edges), f"Expected {len(expected_edges)} edges in topology, got {len(rows)}."
    for expected, actual in zip(expected_edges, rows):
        assert expected == actual, f"Data mismatch. Expected edge {expected}, got {actual}."

    conn.close()

def test_sql_query_performance_and_correctness():
    sql_path = '/home/user/analyze_hierarchy.sql'
    assert os.path.exists(sql_path), f"SQL file {sql_path} does not exist."

    with open(sql_path, 'r') as f:
        query = f.read()

    db_path = '/tmp/test_perf.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE topology (parent_node INTEGER, child_node INTEGER)")

    # Generate a large tree structure (100,000 edges)
    edges = []
    for i in range(1, 100000):
        parent = i // 2  # Binary tree structure
        edges.append((parent, i))

    cur.executemany("INSERT INTO topology VALUES (?, ?)", edges)
    conn.commit()

    start_time = time.time()
    try:
        cur.execute(query)
        results = cur.fetchall()
    except Exception as e:
        pytest.fail(f"SQL execution failed with error: {e}")
    finally:
        conn.close()

    exec_time = time.time() - start_time

    assert len(results) > 0, "Query returned no results."

    dict_res = {row[0]: row[1] for row in results}
    assert dict_res.get(0) == 0, f"Root node 0 should have max_depth 0, got {dict_res.get(0)}"
    assert dict_res.get(99999) == 16, f"Node 99999 should have max_depth 16, got {dict_res.get(99999)}"

    # Metric threshold assertion
    assert exec_time <= 0.5, f"Execution time {exec_time:.4f} seconds exceeds the threshold of 0.5 seconds."