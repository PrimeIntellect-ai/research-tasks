# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/dependency_graph.db"
SCRIPT_PATH = "/home/user/analyze_subgraph.py"
OUTPUT_PATH = "/home/user/output_100.json"

def test_index_created():
    """Verify that the composite index idx_category_score exists."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name='idx_category_score'")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Index 'idx_category_score' is missing from the database"
    index_sql = row[1].lower() if row[1] else ""
    assert "category" in index_sql and "score" in index_sql, "Index 'idx_category_score' does not appear to cover 'category' and 'score'"

def test_script_exists():
    """Verify that the analyze_subgraph.py script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_output_json_validity_and_schema():
    """Verify that output_100.json exists, is valid JSON, and has the correct schema."""
    assert os.path.exists(OUTPUT_PATH), f"Output file missing at {OUTPUT_PATH}"

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON")

    assert isinstance(data, list), "JSON output must be a list of dictionaries"

    for item in data:
        assert isinstance(item, dict), "Each item in the JSON array must be a dictionary"
        for key in ["node_id", "category", "score", "category_rank"]:
            assert key in item, f"Missing key '{key}' in JSON output item: {item}"

def test_output_json_logic():
    """Verify that the output JSON contains the correct nodes and is ordered correctly."""
    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    # The target nodes for source_node 100 are known from the setup
    expected_node_ids = {250, 310, 405, 800, 912}
    actual_node_ids = {item["node_id"] for item in data}

    assert actual_node_ids == expected_node_ids, f"Expected node IDs {expected_node_ids}, but got {actual_node_ids}"

    # Check ordering: rank ascending, then node_id ascending
    for i in range(len(data) - 1):
        current = data[i]
        nxt = data[i+1]

        if current["category_rank"] > nxt["category_rank"]:
            pytest.fail("JSON output is not sorted by category_rank ascending")
        elif current["category_rank"] == nxt["category_rank"]:
            if current["node_id"] > nxt["node_id"]:
                pytest.fail("JSON output is not sorted by node_id ascending when ranks are equal")