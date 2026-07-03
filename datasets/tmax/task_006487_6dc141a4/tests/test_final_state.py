# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/publications.db"
UNOPTIMIZED_PLAN_PATH = "/home/user/plan_unoptimized.txt"
OPTIMIZED_PLAN_PATH = "/home/user/plan_optimized.txt"
COAUTHORS_JSON_PATH = "/home/user/coauthors.json"

def test_files_exist():
    assert os.path.exists(UNOPTIMIZED_PLAN_PATH), f"Missing {UNOPTIMIZED_PLAN_PATH}"
    assert os.path.exists(OPTIMIZED_PLAN_PATH), f"Missing {OPTIMIZED_PLAN_PATH}"
    assert os.path.exists(COAUTHORS_JSON_PATH), f"Missing {COAUTHORS_JSON_PATH}"

def test_unoptimized_plan():
    with open(UNOPTIMIZED_PLAN_PATH, "r") as f:
        content = f.read().upper()
    assert "SCAN" in content, "Unoptimized plan should contain 'SCAN' indicating a full table scan."

def test_optimized_plan():
    with open(OPTIMIZED_PLAN_PATH, "r") as f:
        content = f.read().upper()
    assert "SEARCH" in content or "COVERING INDEX" in content, "Optimized plan should use an index (SEARCH or COVERING INDEX)."

def test_coauthors_json():
    with open(COAUTHORS_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("coauthors.json is not valid JSON")

    assert isinstance(data, list), "coauthors.json must contain a JSON array"

    # Recompute the expected graph directly from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = """
    SELECT a1.author_id, a2.author_id, count(*) 
    FROM wrote a1 
    JOIN wrote a2 ON a1.paper_id = a2.paper_id 
    WHERE a1.author_id < a2.author_id 
    GROUP BY a1.author_id, a2.author_id;
    """
    c.execute(query)
    expected_edges = c.fetchall()
    conn.close()

    expected_dict = {(row[0], row[1]): row[2] for row in expected_edges}

    actual_dict = {}
    for item in data:
        assert isinstance(item, dict), "Each item in the JSON array must be an object"
        assert "source" in item, "Missing 'source' key"
        assert "target" in item, "Missing 'target' key"
        assert "weight" in item, "Missing 'weight' key"

        src = item["source"]
        tgt = item["target"]
        w = item["weight"]
        actual_dict[(src, tgt)] = w

    assert len(actual_dict) == len(expected_dict), f"Expected {len(expected_dict)} edges, but found {len(actual_dict)}"

    for edge, weight in expected_dict.items():
        assert edge in actual_dict, f"Missing edge {edge} in JSON output"
        assert actual_dict[edge] == weight, f"Expected weight {weight} for edge {edge}, got {actual_dict[edge]}"