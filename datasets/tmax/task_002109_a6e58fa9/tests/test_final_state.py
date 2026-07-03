# test_final_state.py

import os
import sqlite3
import json
import csv
import heapq
from collections import defaultdict

def test_network_db_exists():
    """Test that the SQLite database was created."""
    db_path = "/home/user/network.db"
    assert os.path.exists(db_path), f"Missing {db_path}"
    assert os.path.isfile(db_path), f"{db_path} is not a file"

    # Verify it's a valid SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' OR type='view';")
        tables = cursor.fetchall()
        conn.close()
        assert len(tables) > 0, "Database is empty (no tables or views found)."
    except sqlite3.DatabaseError as e:
        assert False, f"Failed to open {db_path} as a SQLite database: {e}"

def test_analysis_result_content():
    """Test the contents of the analysis_result.json file by recomputing expected values."""
    json_path = "/home/user/analysis_result.json"
    assert os.path.exists(json_path), f"Missing {json_path}"

    with open(json_path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON format in {json_path}"

    csv_path = "/home/user/routes.csv"
    assert os.path.exists(csv_path), f"Missing {csv_path} (needed for verification)"

    # Recompute active edges from the CSV
    edges = {}
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u, v = row['source'], row['target']
            dist = float(row['distance'])
            lu = int(row['last_updated'])

            if (u, v) not in edges or edges[(u, v)]['last_updated'] < lu:
                edges[(u, v)] = {'distance': dist, 'last_updated': lu}

    expected_edge_count = len(edges)
    actual_edge_count = res.get("active_edge_count")
    assert actual_edge_count == expected_edge_count, \
        f"Edge count mismatch: expected {expected_edge_count}, got {actual_edge_count}"

    # Recompute shortest path using Dijkstra
    graph = defaultdict(list)
    for (u, v), data in edges.items():
        graph[u].append((v, data['distance']))

    pq = [(0.0, 'S', ['S'])]
    visited = set()
    shortest_path = None
    shortest_dist = None

    while pq:
        dist, node, path = heapq.heappop(pq)

        if node == 'T':
            shortest_path = path
            shortest_dist = dist
            break

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path + [neighbor]))

    actual_path = res.get("shortest_path_S_to_T")
    assert actual_path == shortest_path, \
        f"Shortest path mismatch: expected {shortest_path}, got {actual_path}"

    actual_dist = res.get("shortest_path_distance")
    assert actual_dist is not None, "Missing 'shortest_path_distance' in JSON"
    assert abs(float(actual_dist) - shortest_dist) < 1e-6, \
        f"Shortest path distance mismatch: expected {shortest_dist}, got {actual_dist}"

    # Verify betweenness centrality top 3 nodes
    # (Since full betweenness centrality is complex to implement in pure stdlib, 
    # we verify against the known deterministic output for this dataset)
    expected_top_3 = ["C", "B", "D"]
    actual_top_3 = res.get("top_3_betweenness_nodes", [])
    assert actual_top_3 == expected_top_3, \
        f"Betweenness centrality top 3 mismatch: expected {expected_top_3}, got {actual_top_3}"