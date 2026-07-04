# test_final_state.py

import os
import json
import sqlite3
import time
import subprocess
import heapq
from collections import defaultdict

def test_indexes_created():
    db_path = "/home/user/graph.db"
    assert os.path.exists(db_path), "graph.db not found. Did you re-run db_setup.py?"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = [row[0] for row in cur.fetchall()]
    conn.close()

    assert len(indexes) >= 2, "Indexes on 'edges' table were not created. Did you fix the bug in sqlite-utils and re-run db_setup.py?"

def test_execution_time_and_correctness():
    script_path = "/home/user/optimize_queries.py"
    assert os.path.exists(script_path), f"{script_path} not found."

    # Measure execution time
    start = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"
    assert duration <= 2.0, f"Execution time {duration:.2f}s exceeded threshold of 2.0s. The queries are not optimized enough."

    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"{results_path} not found."

    with open(results_path, "r") as f:
        try:
            student_results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    # Verify correctness by recomputing shortest paths
    db_path = "/home/user/graph.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT source, target, weight FROM edges")
    edges = cur.fetchall()
    conn.close()

    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    pairs_path = "/home/user/pairs.json"
    with open(pairs_path, "r") as f:
        pairs = json.load(f)

    def dijkstra(start_node, end_node):
        queue = [(0, start_node)]
        distances = {start_node: 0}
        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end_node:
                return current_distance

            if current_distance > distances.get(current_node, float('inf')):
                continue

            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return None

    for pair in pairs:
        u, v = pair
        key = f"{u}-{v}"
        expected_weight = dijkstra(u, v)

        assert key in student_results, f"Missing pair {key} in results.json"
        assert student_results[key] == expected_weight, f"Incorrect shortest path weight for {key}. Expected {expected_weight}, got {student_results[key]}"