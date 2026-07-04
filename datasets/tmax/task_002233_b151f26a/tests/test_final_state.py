# test_final_state.py

import os
import sqlite3
import csv
import heapq
import subprocess
import glob
import pytest

DB_PATH = "/home/user/network_topology.db"
CSV_PATH = "/home/user/shortest_paths.csv"
SANITIZER_SCRIPT = "/home/user/query_sanitizer.py"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_corrupted_index_dropped():
    """Verify that the corrupted index 'idx_edges_corrupt' has been dropped."""
    assert os.path.isfile(DB_PATH), f"Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_corrupt';")
    result = cursor.fetchall()
    conn.close()

    assert len(result) == 0, "The corrupted index 'idx_edges_corrupt' still exists in the database."

def compute_expected_paths(db_path, root_node, edge_type):
    """Compute the expected shortest paths using Dijkstra's algorithm."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # By taking MIN(cost), we inherently ignore any stale high-cost duplicate rows
    # that the corrupted index might have caused to be surfaced.
    cursor.execute('''
        SELECT source, target, MIN(cost) 
        FROM edges 
        WHERE edge_type = ? 
        GROUP BY source, target
    ''', (edge_type,))

    graph = {}
    for u, v, cost in cursor.fetchall():
        if u not in graph:
            graph[u] = []
        graph[u].append((v, cost))
    conn.close()

    pq = [(0, root_node, [root_node])]
    distances = {root_node: 0}
    paths = {root_node: [root_node]}

    while pq:
        dist, current, path = heapq.heappop(pq)

        if dist > distances.get(current, float('inf')):
            continue

        for neighbor, weight in graph.get(current, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                paths[neighbor] = path + [neighbor]
                heapq.heappush(pq, (new_dist, neighbor, paths[neighbor]))

    return distances, paths

def test_shortest_paths_csv_correctness():
    """Verify that the shortest paths CSV matches the expected Dijkstra output."""
    assert os.path.isfile(CSV_PATH), f"Shortest paths CSV not found at {CSV_PATH}"

    expected_distances, expected_paths = compute_expected_paths(DB_PATH, 1042, 'FIBER')

    # Remove the root node itself from expected outputs if present, as prompt says "to all other reachable nodes"
    if 1042 in expected_distances:
        del expected_distances[1042]
        del expected_paths[1042]

    actual_distances = {}
    actual_paths = {}

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['target_node_id', 'total_cost', 'path_string'], \
            f"CSV headers are incorrect. Expected ['target_node_id', 'total_cost', 'path_string'], got {reader.fieldnames}"

        for row in reader:
            target = int(row['target_node_id'])
            cost = int(row['total_cost'])
            path_str = row['path_string']

            actual_distances[target] = cost
            actual_paths[target] = path_str

    assert len(actual_distances) > 0, "The generated CSV contains no path data."

    # Validate that all reachable nodes are present and costs/paths match
    missing_nodes = set(expected_distances.keys()) - set(actual_distances.keys())
    assert not missing_nodes, f"CSV is missing shortest paths for nodes: {missing_nodes}"

    for node, expected_cost in expected_distances.items():
        assert actual_distances[node] == expected_cost, \
            f"Incorrect cost for target node {node}. Expected {expected_cost}, got {actual_distances[node]}."

        expected_path_str = "->".join(map(str, expected_paths[node]))
        assert actual_paths[node] == expected_path_str, \
            f"Incorrect path string for target node {node}. Expected {expected_path_str}, got {actual_paths[node]}."

def test_query_sanitizer_adversarial_corpus():
    """Verify the query sanitizer correctly accepts clean queries and rejects evil queries."""
    assert os.path.isfile(SANITIZER_SCRIPT), f"Query sanitizer script not found at {SANITIZER_SCRIPT}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))

    assert len(clean_files) > 0, "No clean corpus files found to test."
    assert len(evil_files) > 0, "No evil corpus files found to test."

    clean_failed = []
    evil_bypassed = []

    # Test Clean Corpus (Expected Exit Code 0)
    for clean_file in clean_files:
        result = subprocess.run(["python3", SANITIZER_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(clean_file))

    # Test Evil Corpus (Expected Exit Code 1)
    for evil_file in evil_files:
        result = subprocess.run(["python3", SANITIZER_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))