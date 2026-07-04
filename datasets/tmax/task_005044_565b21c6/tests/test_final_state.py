# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/network.db"
SCRIPT_PATH = "/home/user/etl_pipeline.sh"
JSON_PATH = "/home/user/graph.json"
METRICS_PATH = "/home/user/metrics.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script file {SCRIPT_PATH} is missing."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script file {SCRIPT_PATH} is not executable."

def test_index_created():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list('edges');")
    indexes = [row[1] for row in cursor.fetchall()]
    assert 'idx_source_weight' in indexes, "Index 'idx_source_weight' was not created on the 'edges' table."

    # Optional: verify columns in the index
    cursor.execute("PRAGMA index_info('idx_source_weight');")
    columns = [row[2] for row in cursor.fetchall()]
    assert 'source_id' in columns and 'weight' in columns, "Index 'idx_source_weight' does not cover the correct columns."
    conn.close()

def test_top_edges_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='top_edges';")
    assert cursor.fetchone() is not None, "Table 'top_edges' is missing in the database."

    cursor.execute("SELECT source_id, target_id, weight FROM top_edges ORDER BY source_id, target_id;")
    actual_top_edges = cursor.fetchall()
    conn.close()

    expected_top_edges = [
        (1, 2, 10), (1, 4, 15),
        (2, 1, 8), (2, 4, 12),
        (3, 1, 20), (3, 5, 25),
        (4, 2, 5), (4, 5, 5)
    ]

    assert actual_top_edges == expected_top_edges, f"Data in 'top_edges' is incorrect. Expected {expected_top_edges}, got {actual_top_edges}"

def test_graph_json():
    assert os.path.isfile(JSON_PATH), f"JSON file {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert "nodes" in data, "JSON output missing 'nodes' key."
    assert "edges" in data, "JSON output missing 'edges' key."

    expected_nodes = [
        {"id": 1, "label": "Node1", "category": "Alpha"},
        {"id": 2, "label": "Node2", "category": "Alpha"},
        {"id": 3, "label": "Node3", "category": "Beta"},
        {"id": 4, "label": "Node4", "category": "Beta"},
        {"id": 5, "label": "Node5", "category": "Gamma"}
    ]

    expected_edges = [
        {"source": 1, "target": 2, "weight": 10},
        {"source": 1, "target": 4, "weight": 15},
        {"source": 2, "target": 1, "weight": 8},
        {"source": 2, "target": 4, "weight": 12},
        {"source": 3, "target": 1, "weight": 20},
        {"source": 3, "target": 5, "weight": 25},
        {"source": 4, "target": 2, "weight": 5},
        {"source": 4, "target": 5, "weight": 5}
    ]

    actual_nodes = sorted(data["nodes"], key=lambda x: x.get("id", 0))
    actual_edges = sorted(data["edges"], key=lambda x: (x.get("source", 0), x.get("target", 0)))

    assert actual_nodes == expected_nodes, "JSON 'nodes' data is incorrect."
    assert actual_edges == expected_edges, "JSON 'edges' data is incorrect."

def test_metrics_txt():
    assert os.path.isfile(METRICS_PATH), f"Metrics file {METRICS_PATH} is missing."

    with open(METRICS_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Category: Alpha, Total Weight: 68",
        "Category: Beta, Total Weight: 55"
    ]

    assert lines == expected_lines, f"Contents of {METRICS_PATH} are incorrect. Expected {expected_lines}, got {lines}"