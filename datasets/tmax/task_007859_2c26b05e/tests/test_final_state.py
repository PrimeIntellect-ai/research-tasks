# test_final_state.py

import os
import sqlite3
import csv
import math
import subprocess
import pytest

def test_mongo_setup():
    # Check if mongo data directory and log file exist
    data_dir = "/home/user/mongo_data"
    log_file = "/home/user/mongo.log"

    assert os.path.exists(data_dir) and os.path.isdir(data_dir), f"MongoDB data directory {data_dir} is missing or not a directory."
    assert os.path.exists(log_file) and os.path.isfile(log_file), f"MongoDB log file {log_file} is missing or not a file."

    # Check if mongod is running
    try:
        subprocess.check_output(["pgrep", "mongod"])
    except subprocess.CalledProcessError:
        pytest.fail("mongod process is not running.")

def test_sqlite_db_schema_and_data():
    db_path = "/home/user/warehouse.db"
    assert os.path.exists(db_path), f"SQLite database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row['name'] for row in cursor.fetchall()}
    assert 'nodes' in tables, "Table 'nodes' is missing in warehouse.db"
    assert 'edges' in tables, "Table 'edges' is missing in warehouse.db"

    # Check edges data
    cursor.execute("SELECT sender, receiver, volume FROM edges;")
    edges = cursor.fetchall()

    expected_edges = {
        ("A", "B", 70.0),
        ("B", "C", 100.0),
        ("C", "A", 80.0),
        ("D", "B", 200.0),
        ("A", "D", 300.0),
        ("D", "E", 60.0),
        ("E", "A", 70.0)
    }

    actual_edges = set()
    for row in edges:
        actual_edges.add((row['sender'], row['receiver'], float(row['volume'])))

    assert actual_edges == expected_edges, f"Edges in warehouse.db do not match expected filtered aggregation. Got {actual_edges}"

    # Check nodes data (PageRank)
    cursor.execute("SELECT node_id, pagerank FROM nodes;")
    nodes = cursor.fetchall()

    expected_nodes = {"A", "B", "C", "D", "E"}
    actual_nodes = {row['node_id'] for row in nodes}

    assert actual_nodes == expected_nodes, f"Nodes in warehouse.db do not match expected entities. Got {actual_nodes}"

    # PageRank values should be valid floats between 0 and 1
    for row in nodes:
        pr = float(row['pagerank'])
        assert 0 < pr < 1, f"PageRank for node {row['node_id']} is out of bounds: {pr}"

    conn.close()

def test_result_csv():
    csv_path = "/home/user/result.csv"
    assert os.path.exists(csv_path), f"Result CSV {csv_path} is missing."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        expected_fields = ["sender", "receiver", "volume", "combined_pagerank"]
        assert fieldnames == expected_fields, f"CSV headers do not match. Expected {expected_fields}, got {fieldnames}"

        rows = list(reader)
        assert len(rows) == 1, f"Expected exactly 1 row in result.csv, got {len(rows)}"

        row = rows[0]
        assert row['sender'] == 'A', f"Expected sender 'A', got {row['sender']}"
        assert row['receiver'] == 'D', f"Expected receiver 'D', got {row['receiver']}"
        assert float(row['volume']) == 300.0, f"Expected volume 300.0, got {row['volume']}"

        combined_pr = float(row['combined_pagerank'])
        assert math.isclose(combined_pr, 0.5630, abs_tol=0.005), f"Combined PageRank {combined_pr} is not within tolerance of 0.5630"