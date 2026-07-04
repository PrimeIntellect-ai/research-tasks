# test_final_state.py

import os
import json
import sqlite3
import pytest
from collections import defaultdict, deque

def compute_expected_results():
    db_path = "/home/user/audit/active.sqlite"
    json_path = "/home/user/audit/archived.json"

    edges = set()
    nodes = set()

    # Read SQLite
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT src_account, dst_account FROM transfers")
        for src, dst in cur.fetchall():
            edges.add((src, dst))
            nodes.add(src)
            nodes.add(dst)
        conn.close()

    # Read JSON
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            for row in data:
                src = row.get("from_account")
                dst = row.get("to_account")
                if src and dst:
                    edges.add((src, dst))
                    nodes.add(src)
                    nodes.add(dst)

    # Build adjacency lists
    adj = defaultdict(list)
    in_degree = defaultdict(int)

    for src, dst in edges:
        adj[src].append(dst)
        in_degree[dst] += 1

    # Shortest path using BFS
    start = "C-837"
    target = "C-102"

    queue = deque([[start]])
    visited = set([start])
    shortest_path = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            shortest_path = path
            break

        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    path_hops = len(shortest_path) - 1 if shortest_path else 0

    # In-Degree Centrality
    N = len(nodes)
    centrality = {}
    for node in nodes:
        centrality[node] = in_degree[node] / (N - 1) if N > 1 else 0

    # Bottleneck node
    bottleneck_account = None
    bottleneck_centrality = -1

    if len(shortest_path) > 2:
        for node in shortest_path[1:-1]:
            if centrality[node] > bottleneck_centrality:
                bottleneck_centrality = centrality[node]
                bottleneck_account = node

    return {
        "shortest_path": shortest_path,
        "path_hops": path_hops,
        "bottleneck_account": bottleneck_account,
        "bottleneck_centrality": round(bottleneck_centrality, 4) if bottleneck_centrality != -1 else 0.0
    }

def test_compliance_report():
    report_path = "/home/user/compliance_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected = compute_expected_results()

    assert "shortest_path" in report, "Missing 'shortest_path' in report."
    assert report["shortest_path"] == expected["shortest_path"], f"Expected shortest_path {expected['shortest_path']}, got {report['shortest_path']}"

    assert "path_hops" in report, "Missing 'path_hops' in report."
    assert report["path_hops"] == expected["path_hops"], f"Expected path_hops {expected['path_hops']}, got {report['path_hops']}"

    assert "bottleneck_account" in report, "Missing 'bottleneck_account' in report."
    assert report["bottleneck_account"] == expected["bottleneck_account"], f"Expected bottleneck_account {expected['bottleneck_account']}, got {report['bottleneck_account']}"

    assert "bottleneck_centrality" in report, "Missing 'bottleneck_centrality' in report."
    assert report["bottleneck_centrality"] == expected["bottleneck_centrality"], f"Expected bottleneck_centrality {expected['bottleneck_centrality']}, got {report['bottleneck_centrality']}"