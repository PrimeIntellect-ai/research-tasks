# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_analyze_script_exists():
    assert os.path.isfile('/home/user/analyze.py'), "analyze.py script is missing."

def test_database_exists_and_schema():
    db_path = '/home/user/network.db'
    assert os.path.isfile(db_path), "network.db database is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert 'nodes' in tables, "Table 'nodes' is missing in network.db."
    assert 'edges' in tables, "Table 'edges' is missing in network.db."

    # Check nodes data
    cursor.execute("SELECT count(*) FROM nodes;")
    node_count = cursor.fetchone()[0]
    assert node_count == 8, f"Expected 8 rows in nodes table, got {node_count}."

    # Check edges data
    cursor.execute("SELECT count(*) FROM edges;")
    edge_count = cursor.fetchone()[0]
    assert edge_count == 10, f"Expected 10 rows in edges table, got {edge_count}."

    conn.close()

def test_report_json_content():
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), "report.json is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    assert 'top_per_dept' in data, "Key 'top_per_dept' missing in report.json."
    assert 'triangles' in data, "Key 'triangles' missing in report.json."

    top_per_dept = data['top_per_dept']
    assert top_per_dept.get('HR') == 1, f"Expected HR top employee to be 1, got {top_per_dept.get('HR')}"
    assert top_per_dept.get('IT') == 3, f"Expected IT top employee to be 3, got {top_per_dept.get('IT')}"
    assert top_per_dept.get('Sales') == 6, f"Expected Sales top employee to be 6, got {top_per_dept.get('Sales')}"

    expected_triangles = [[3, 4, 5], [6, 7, 8]]
    actual_triangles = [sorted(t) for t in data['triangles']]

    assert len(actual_triangles) == 2, f"Expected 2 triangles, got {len(actual_triangles)}."
    for t in expected_triangles:
        assert t in actual_triangles, f"Missing expected triangle {t} in report.json."