# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

def test_database_exists():
    db_path = "/home/user/logistics.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    # Check table schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='node_metrics'")
    assert cursor.fetchone() is not None, "Table 'node_metrics' does not exist in the database."
    conn.close()

def test_query_plan_exists():
    qp_path = "/home/user/query_plan.txt"
    assert os.path.isfile(qp_path), f"Query plan file {qp_path} does not exist."

    with open(qp_path, 'r') as f:
        content = f.read().upper()
        # EXPLAIN QUERY PLAN usually contains words like SCAN, SEARCH, or USE TEMP B-TREE
        assert any(keyword in content for keyword in ["SCAN", "SEARCH", "B-TREE", "LIST"]), \
            "query_plan.txt does not look like the output of EXPLAIN QUERY PLAN."

def test_result_json_validity_and_invariants():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert isinstance(data, list), "Result JSON must be an array."
    assert len(data) == 5, f"Expected exactly 5 results (page 2, size 5), got {len(data)}."

    prev_pr = float('inf')
    prev_id = ""

    for item in data:
        assert isinstance(item, dict), "Each item in the result array must be an object."
        assert "node_id" in item, "Missing 'node_id'."
        assert "node_type" in item, "Missing 'node_type'."
        assert "pagerank" in item, "Missing 'pagerank'."
        assert "community_id" in item, "Missing 'community_id'."

        assert item["node_type"] == "Distribution Center", \
            f"Expected node_type 'Distribution Center', got {item['node_type']}."
        assert item["pagerank"] > 0.01, \
            f"Expected pagerank > 0.01, got {item['pagerank']}."

        # Check sorting: pagerank DESC, node_id ASC
        pr = item["pagerank"]
        nid = item["node_id"]

        if pr > prev_pr:
            pytest.fail("Results are not sorted descending by pagerank.")
        elif pr == prev_pr:
            if nid < prev_id:
                pytest.fail("Tied pageranks are not sorted ascending by node_id.")

        prev_pr = pr
        prev_id = nid

def test_validate_script_runs():
    validate_path = "/home/user/validate.py"
    assert os.path.isfile(validate_path), f"Validation script {validate_path} does not exist."

    result = subprocess.run(
        ["python3", validate_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, \
        f"validate.py failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"