# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_indexes_created():
    db_path = "/home/user/network.db"
    assert os.path.exists(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all indexes on the edges table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes were created on the 'edges' table."

    indexed_columns = set()
    for (idx_name,) in indexes:
        # Avoid SQL injection by checking if it's a valid identifier, though it's from sqlite_master
        cursor.execute(f'PRAGMA index_info("{idx_name}");')
        info = cursor.fetchall()
        for col_info in info:
            # col_info is (seqno, cid, name)
            col_name = col_info[2]
            if col_name:
                indexed_columns.add(col_name)

    conn.close()

    assert 'source' in indexed_columns or 'target' in indexed_columns, \
        "Expected an index on 'source' or 'target' columns of the 'edges' table to optimize the query."

def test_report_json_correctness():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    assert isinstance(data, list), "The JSON root must be a list of objects."
    assert len(data) == 3, f"Expected exactly 3 items in report.json, found {len(data)}."

    for i, item in enumerate(data):
        assert "node_name" in item, f"Item at index {i} is missing 'node_name'."
        assert "pagerank" in item, f"Item at index {i} is missing 'pagerank'."
        assert isinstance(item["node_name"], str), f"'node_name' at index {i} must be a string."
        assert isinstance(item["pagerank"], (int, float)), f"'pagerank' at index {i} must be a number."

    # Check that pageranks are sorted descending
    assert data[0]["pagerank"] >= data[1]["pagerank"], "PageRank values are not sorted in descending order."
    assert data[1]["pagerank"] >= data[2]["pagerank"], "PageRank values are not sorted in descending order."

    # Based on the graph structure, Echo Hub is the most central, followed by Alpha
    assert data[0]["node_name"] == "Echo Hub", f"Expected top node to be 'Echo Hub', got '{data[0]['node_name']}'."
    assert data[1]["node_name"] == "Alpha", f"Expected second node to be 'Alpha', got '{data[1]['node_name']}'."