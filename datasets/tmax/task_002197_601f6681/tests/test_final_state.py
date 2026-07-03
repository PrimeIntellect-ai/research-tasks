# test_final_state.py

import os
import sqlite3
import json
import csv
import pytest

def test_fixed_query_file():
    fixed_query_path = "/home/user/fixed_query.sql"
    assert os.path.isfile(fixed_query_path), f"File {fixed_query_path} does not exist."
    with open(fixed_query_path, 'r') as f:
        content = f.read().lower()
        assert "join" in content, "fixed_query.sql must use standard JOINs."
        assert "over" in content, "fixed_query.sql must use a Window Function (like ROW_NUMBER() OVER(...))."

def test_indexes_applied():
    db_path = "/home/user/network.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('edges');")
    edges_indexes = cursor.fetchall()

    cursor.execute("PRAGMA index_list('nodes');")
    nodes_indexes = cursor.fetchall()

    assert len(edges_indexes) > 0 or len(nodes_indexes) > 0, "No indexes were applied to the edges or nodes tables."
    conn.close()

    indexes_path = "/home/user/indexes.sql"
    assert os.path.isfile(indexes_path), f"File {indexes_path} does not exist."

def test_recent_edges_csv():
    csv_path = "/home/user/recent_edges.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 6, f"Expected 6 rows in CSV, found {len(rows)}."

    # Check that cross-region edge is excluded (source 1, target 6)
    for row in rows:
        assert not (row['source'] == '1' and row['target'] == '6'), "Cross-region edge should be excluded."

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not valid JSON.")

    assert "shortest_path" in report, "report.json missing 'shortest_path' key."
    assert "max_degree_node" in report, "report.json missing 'max_degree_node' key."

    assert report["max_degree_node"] == 3, f"Expected max_degree_node to be 3, got {report['max_degree_node']}."

    path = report["shortest_path"]
    assert isinstance(path, list), "shortest_path must be a list."
    assert len(path) == 3, f"Expected shortest_path length 3, got {len(path)}."
    assert path[0] == 1, f"Expected shortest_path to start with 1, got {path[0]}."
    assert path[-1] == 5, f"Expected shortest_path to end with 5, got {path[-1]}."
    assert path[1] in [2, 3], f"Expected intermediate node to be 2 or 3, got {path[1]}."

def test_graph_analytics_script():
    script_path = "/home/user/graph_analytics.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."