# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/graph_backup.db"
SUMMARY_PATH = "/home/user/stale_summary.txt"
CYPHER_PATH = "/home/user/cleanup.cypher"
SCRIPT_PATH = "/home/user/analyze_graph.py"

def get_stale_edges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT e.edge_id, e.source_id, e.rel_type 
        FROM edges e 
        JOIN nodes n ON e.source_id = n.node_id 
        WHERE e.target_id NOT IN (SELECT node_id FROM nodes)
        ORDER BY e.edge_id ASC
    """
    cursor.execute(query)
    stale_edges = cursor.fetchall()
    conn.close()
    return stale_edges

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} was not created."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_stale_summary():
    assert os.path.exists(SUMMARY_PATH), f"Summary file {SUMMARY_PATH} is missing."

    stale_edges = get_stale_edges()
    counts = {}
    for _, _, rel_type in stale_edges:
        counts[rel_type] = counts.get(rel_type, 0) + 1

    expected_lines = [f"{rel}: {counts[rel]}" for rel in sorted(counts.keys())]

    with open(SUMMARY_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {SUMMARY_PATH} do not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_cleanup_cypher():
    assert os.path.exists(CYPHER_PATH), f"Cypher script {CYPHER_PATH} is missing."

    stale_edges = get_stale_edges()
    expected_lines = []
    for edge_id, source_id, rel_type in stale_edges:
        line = f"MATCH (s)-[r:{rel_type}]->() WHERE s.node_id = {source_id} AND r.edge_backup_id = {edge_id} DELETE r;"
        expected_lines.append(line)

    with open(CYPHER_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {CYPHER_PATH} do not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )