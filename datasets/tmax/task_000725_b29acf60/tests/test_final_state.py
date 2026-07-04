# test_final_state.py

import os
import json
import re
import pytest

def test_results_json_exists_and_correct():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Expected results file at {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {path}."

    # Check expected math:
    # Node 1: 1->2->3, 1->2->4 (2 paths)
    # Node 2: 2->3->5, 2->4->5 (2 paths)
    # Others: 0 paths or missing.

    node_counts = {item.get("node_id"): item.get("path_count") for item in data}

    assert node_counts.get(1) == 2, "Node 1 should have exactly 2 length-2 paths."
    assert node_counts.get(2) == 2, "Node 2 should have exactly 2 length-2 paths."

    for node_id in [3, 4, 5]:
        if node_id in node_counts:
            assert node_counts[node_id] == 0, f"Node {node_id} should have 0 length-2 paths."

def test_plan_txt_exists_and_contains_plan():
    path = "/home/user/plan.txt"
    assert os.path.isfile(path), f"Expected query plan file at {path} does not exist."

    with open(path, "r") as f:
        content = f.read().upper()

    # SQLite EXPLAIN QUERY PLAN typically outputs SCAN, SEARCH, or USE TEMP B-TREE
    assert "SCAN" in content or "SEARCH" in content or "QUERY PLAN" in content, \
        f"{path} does not appear to contain a valid SQLite query plan."

def test_analyze_go_uses_explicit_join():
    path = "/home/user/analyze.go"
    assert os.path.isfile(path), f"Expected Go script at {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check that there is no comma-separated FROM clause like `FROM nodes n, edges e1, edges e2`
    # and that JOIN is used.
    assert re.search(r'\bJOIN\b', content, re.IGNORECASE), "analyze.go must use explicit JOIN syntax."
    assert not re.search(r'FROM\s+\w+\s+\w+\s*,\s*\w+\s+\w+\s*,\s*\w+\s+\w+', content, re.IGNORECASE), \
        "analyze.go must not use implicit cross joins (comma-separated tables in FROM clause)."