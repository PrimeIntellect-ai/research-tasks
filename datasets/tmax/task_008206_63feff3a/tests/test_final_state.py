# test_final_state.py
import os
import json
import sqlite3
import pytest

OUTPUT_PATH = '/home/user/unified_graph.json'
DB_PATH = '/home/user/research_data.db'
JSONL_PATH = '/home/user/metadata.jsonl'

@pytest.fixture(scope="module")
def output_data():
    assert os.path.exists(OUTPUT_PATH), f"Output file missing at {OUTPUT_PATH}"
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file is not valid JSON: {e}")
    return data

def test_original_files_unmodified():
    # Check DB
    assert os.path.exists(DB_PATH), "Original database file is missing"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM subjects")
    assert c.fetchone()[0] == 4, "Subjects table was modified"
    c.execute("SELECT COUNT(*) FROM measurements")
    assert c.fetchone()[0] == 5, "Measurements table was modified"
    conn.close()

    # Check JSONL
    assert os.path.exists(JSONL_PATH), "Original JSONL file is missing"
    with open(JSONL_PATH, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 4, "metadata.jsonl was modified"

def test_output_schema_and_sorting(output_data):
    assert "nodes" in output_data, "Missing 'nodes' key in output"
    assert "edges" in output_data, "Missing 'edges' key in output"

    nodes = output_data["nodes"]
    edges = output_data["edges"]

    assert isinstance(nodes, list), "'nodes' must be a list"
    assert isinstance(edges, list), "'edges' must be a list"

    # Check nodes sorting
    ids = [n.get("id") for n in nodes]
    assert all(isinstance(i, int) for i in ids), "Node IDs must be integers"
    assert ids == sorted(ids), "Nodes are not sorted by id ascending"

    # Check edges sorting
    edge_tuples = [(e.get("source"), e.get("target")) for e in edges]
    assert all(isinstance(s, int) and isinstance(t, int) for s, t in edge_tuples), "Edge source/target must be integers"
    assert edge_tuples == sorted(edge_tuples), "Edges are not sorted by source then target"

def test_nodes_latest_values(output_data):
    nodes = {n["id"]: n for n in output_data["nodes"]}

    assert 1 in nodes
    assert nodes[1]["latest_value"] == 12.0, "Node 1 latest_value is incorrect (did you use the stale cache?)"
    assert nodes[1]["name"] == "Alpha"
    assert nodes[1]["attributes"] == {"type": "control", "age": 30}

    assert 2 in nodes
    assert nodes[2]["latest_value"] == 8.2

    assert 3 in nodes
    assert nodes[3]["latest_value"] == 14.8, "Node 3 latest_value is incorrect (did you use the stale cache?)"

    assert 4 in nodes
    assert nodes[4]["latest_value"] is None, "Node 4 latest_value should be null/None"

def test_edges_dangling_removed(output_data):
    edges = output_data["edges"]
    edge_tuples = [(e["source"], e["target"]) for e in edges]

    # 3 -> 99 should be removed because 99 is not in subjects
    assert (3, 99) not in edge_tuples, "Dangling edge (3 -> 99) was not removed"

    # Valid edges should be present
    expected_edges = [(1, 2), (1, 3), (2, 3), (3, 4), (4, 1)]
    for edge in expected_edges:
        assert edge in edge_tuples, f"Missing expected edge {edge}"

    assert len(edge_tuples) == len(expected_edges), "Output contains unexpected extra edges"