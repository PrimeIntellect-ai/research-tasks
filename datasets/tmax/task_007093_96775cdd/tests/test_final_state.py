# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/components.db'
JSON_PATH = '/home/user/summary.json'

def test_summary_json_exists_and_correct():
    assert os.path.exists(JSON_PATH), f"Output file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} does not contain valid JSON.")

    assert "total_downstream_nodes" in data, "Missing 'total_downstream_nodes' in JSON."
    assert data["total_downstream_nodes"] == 5, f"Expected 5 total downstream nodes, got {data['total_downstream_nodes']}."

    assert "cost_by_type" in data, "Missing 'cost_by_type' in JSON."
    cost_by_type = data["cost_by_type"]

    assert "library" in cost_by_type, "Missing 'library' type in cost_by_type."
    assert "service" in cost_by_type, "Missing 'service' type in cost_by_type."

    assert cost_by_type["library"] == 25.5, f"Expected library cost 25.5, got {cost_by_type['library']}."
    assert cost_by_type["service"] == 105.0, f"Expected service cost 105.0, got {cost_by_type['service']}."

def test_index_created_on_edges():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if an index exists on edges(source) or edges(source, target)
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = c.fetchall()

    valid_index_found = False
    for name, sql in indexes:
        if sql and 'source' in sql.lower():
            valid_index_found = True
            break

    conn.close()

    assert valid_index_found, "No optimal index found on the 'edges' table covering the 'source' column."