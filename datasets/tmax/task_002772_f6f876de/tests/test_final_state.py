# test_final_state.py

import os
import json
import sqlite3
import pytest
from collections import deque

def test_final_results_json():
    db_path = "/home/user/research_data.db"
    json_path = "/home/user/path_results.json"

    assert os.path.exists(json_path), f"Output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load nodes
    cursor.execute("SELECT node_id, p_title, p_year FROM tbl_nodes")
    nodes = {row[0]: {"title": row[1], "year": row[2]} for row in cursor.fetchall()}

    # Load edges
    cursor.execute("SELECT from_node, to_node FROM tbl_edges")
    edges = cursor.fetchall()

    # Load authors
    cursor.execute("SELECT node_id, creator_name FROM tbl_creators")
    authors = {}
    for row in cursor.fetchall():
        authors.setdefault(row[0], []).append(row[1])

    for node_id in authors:
        authors[node_id].sort()

    # Identify start and end nodes
    start_id = None
    end_id = None
    for nid, ndata in nodes.items():
        if ndata["title"] == "Quantum Origins":
            start_id = nid
        elif ndata["title"] == "Macroscopic Superposition":
            end_id = nid

    assert start_id is not None, "Start node 'Quantum Origins' missing in DB."
    assert end_id is not None, "End node 'Macroscopic Superposition' missing in DB."

    # Build adjacency list and find shortest path using BFS
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)

    queue = deque([[start_id]])
    visited = {start_id}
    shortest_path = None

    while queue:
        path = queue.popleft()
        curr = path[-1]
        if curr == end_id:
            shortest_path = path
            break

        for nxt in adj.get(curr, []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])

    assert shortest_path is not None, "No path found between start and end nodes in DB."

    # Construct expected JSON structure
    expected_data = []
    for nid in shortest_path:
        expected_data.append({
            "title": nodes[nid]["title"],
            "year": nodes[nid]["year"],
            "authors": authors.get(nid, [])
        })

    assert actual_data == expected_data, (
        f"JSON content does not match the expected shortest path.\n"
        f"Expected: {json.dumps(expected_data, indent=2)}\n"
        f"Actual: {json.dumps(actual_data, indent=2)}"
    )