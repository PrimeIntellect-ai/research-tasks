# test_final_state.py

import os
import sqlite3
import json
import heapq

def get_expected_path_and_latency():
    db_path = '/home/user/backup_metadata.db'
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get datacenters with a successful backup job
    cursor.execute("SELECT dc_id FROM backup_jobs WHERE status = 'SUCCESS'")
    successful_dcs = set(row[0] for row in cursor.fetchall())

    # Get all replication links
    cursor.execute("SELECT source_id, target_id, latency_ms FROM replication_links")
    edges = cursor.fetchall()
    conn.close()

    # Build adjacency list filtering by target's backup status
    graph = {}
    for src, tgt, lat in edges:
        if tgt in successful_dcs:
            if src not in graph:
                graph[src] = []
            graph[src].append((tgt, lat))

    # Dijkstra's algorithm from DC-Alpha (1) to DC-Omega (4)
    start = 1
    end = 4

    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node == end:
            return path, cost

        if node in visited:
            continue

        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return None, None

def test_cpp_file_exists():
    assert os.path.isfile('/home/user/backup_analyzer.cpp'), "/home/user/backup_analyzer.cpp is missing."

def test_executable_exists():
    executable_path = '/home/user/backup_analyzer'
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing. Did you compile the C++ program?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_json_output():
    json_path = '/home/user/optimal_backup_path.json'
    assert os.path.isfile(json_path), f"Output file {json_path} is missing. Did you run the compiled executable?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert 'path' in data, "The 'path' key is missing in the JSON output."
    assert 'total_latency_ms' in data, "The 'total_latency_ms' key is missing in the JSON output."

    expected_path, expected_latency = get_expected_path_and_latency()

    assert expected_path is not None, "Could not find a valid path in the database. Was the database modified incorrectly?"

    assert data['path'] == expected_path, f"Incorrect path. Expected {expected_path}, but got {data['path']}."
    assert data['total_latency_ms'] == expected_latency, f"Incorrect total latency. Expected {expected_latency}, but got {data['total_latency_ms']}."