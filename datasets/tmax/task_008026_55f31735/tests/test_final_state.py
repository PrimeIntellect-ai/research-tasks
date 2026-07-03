# test_final_state.py

import os
import json
import csv
import sqlite3
import pytest

DATA_FILE = "/home/user/data/transactions.jsonl"
EDGES_CSV = "/home/user/data/edges.csv"
DB_FILE = "/home/user/db/graph.sqlite"
RESULTS_CSV = "/home/user/results/top_paths.csv"

def get_expected_edges():
    edges = []
    if not os.path.exists(DATA_FILE):
        return edges
    with open(DATA_FILE, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("event_type") == "transfer" and record.get("status") == "success":
                edges.append({
                    "source": record["sender"],
                    "target": record["receiver"],
                    "timestamp": record["timestamp"],
                    "amount": record["amount"]
                })
    return edges

def get_expected_top_paths():
    edges = get_expected_edges()

    # Build 3-hop paths
    paths = []
    for e1 in edges:
        for e2 in edges:
            if e1["target"] == e2["source"] and e1["timestamp"] < e2["timestamp"]:
                for e3 in edges:
                    if e2["target"] == e3["source"] and e2["timestamp"] < e3["timestamp"]:
                        paths.append({
                            "start_node": e1["source"],
                            "end_node": e3["target"],
                            "total_amount": e1["amount"] + e2["amount"] + e3["amount"]
                        })

    # Rank by total_amount descending partitioned by start_node
    best_paths = {}
    for p in paths:
        sn = p["start_node"]
        if sn not in best_paths or p["total_amount"] > best_paths[sn]["total_amount"]:
            best_paths[sn] = p

    # Sort globally by total_amount desc, take top 5
    sorted_paths = sorted(best_paths.values(), key=lambda x: x["total_amount"], reverse=True)
    return sorted_paths[:5]

def test_edges_csv_exists_and_correct():
    assert os.path.isfile(EDGES_CSV), f"Edges CSV file is missing: {EDGES_CSV}"

    expected_edges = get_expected_edges()

    with open(EDGES_CSV, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        assert headers == ["source", "target", "timestamp", "amount"], f"Incorrect headers in {EDGES_CSV}"

        rows = list(reader)
        assert len(rows) == len(expected_edges), f"Expected {len(expected_edges)} edges, found {len(rows)}"

        # Check a few records if possible
        for row, exp in zip(rows, expected_edges):
            assert row["source"] == exp["source"]
            assert row["target"] == exp["target"]
            assert int(row["timestamp"]) == exp["timestamp"]
            assert float(row["amount"]) == exp["amount"]

def test_database_and_schema():
    assert os.path.isfile(DB_FILE), f"Database file is missing: {DB_FILE}"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Edges'")
    assert cursor.fetchone() is not None, "Table 'Edges' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(Edges)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert "source" in columns, "Column 'source' missing"
    assert "target" in columns, "Column 'target' missing"
    assert "timestamp" in columns, "Column 'timestamp' missing"
    assert "amount" in columns, "Column 'amount' missing"

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='Edges'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on the Edges table. Indexes are required for optimization."

    # Check data loaded
    cursor.execute("SELECT COUNT(*) FROM Edges")
    count = cursor.fetchone()[0]
    expected_count = len(get_expected_edges())
    assert count == expected_count, f"Expected {expected_count} rows in Edges table, found {count}"

    conn.close()

def test_results_csv_exists_and_correct():
    assert os.path.isfile(RESULTS_CSV), f"Results CSV file is missing: {RESULTS_CSV}"

    expected_paths = get_expected_top_paths()

    with open(RESULTS_CSV, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ["start_node", "end_node", "total_amount"], f"Incorrect headers in {RESULTS_CSV}"

        rows = list(reader)
        assert len(rows) == len(expected_paths), f"Expected {len(expected_paths)} paths, found {len(rows)}"

        for i, (row, exp) in enumerate(zip(rows, expected_paths)):
            assert row[0] == exp["start_node"], f"Row {i+1}: expected start_node {exp['start_node']}, got {row[0]}"
            assert row[1] == exp["end_node"], f"Row {i+1}: expected end_node {exp['end_node']}, got {row[1]}"
            assert float(row[2]) == exp["total_amount"], f"Row {i+1}: expected total_amount {exp['total_amount']}, got {row[2]}"