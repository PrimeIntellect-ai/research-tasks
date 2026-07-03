# test_final_state.py

import os
import csv
import json
import time
import heapq
import subprocess
import pytest

def get_true_shortest_path(csv_path, start_node, end_node):
    graph = {}
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3: 
                continue
            try:
                u, v, w = int(row[0]), int(row[1]), float(row[2])
                if u not in graph: 
                    graph[u] = []
                graph[u].append((v, w))
            except ValueError:
                # Skip header row if present
                pass

    pq = [(0.0, start_node, [start_node])]
    visited = set()

    while pq:
        w, u, path = heapq.heappop(pq)
        if u in visited: 
            continue
        visited.add(u)

        if u == end_node:
            return path, w

        for v, weight in graph.get(u, []):
            if v not in visited:
                heapq.heappush(pq, (w + weight, v, path + [v]))

    return None, None

def test_pipeline_and_fast_query():
    start_node = 452
    end_node = 8910
    csv_path = '/app/interactions.csv'

    assert os.path.isfile(csv_path), f"Missing interactions dataset at {csv_path}"

    # 1. Compute truth
    best_path, best_weight = get_true_shortest_path(csv_path, start_node, end_node)
    assert best_path is not None, f"No path found between {start_node} and {end_node} in truth data"

    # 2. Check final_result.json correctness
    json_path = '/home/user/final_result.json'
    assert os.path.isfile(json_path), f"Missing final JSON output at {json_path}"

    with open(json_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON")

    assert result.get("start") == start_node, f"Expected start node {start_node}, got {result.get('start')}"
    assert result.get("end") == end_node, f"Expected end node {end_node}, got {result.get('end')}"
    assert result.get("path") == best_path, f"Expected path {best_path}, got {result.get('path')}"

    actual_weight = result.get("total_weight")
    assert actual_weight is not None, "Missing 'total_weight' in JSON output"
    assert abs(float(actual_weight) - best_weight) < 1e-4, f"Expected weight {best_weight}, got {actual_weight}"

    # 3. Benchmark the compiled C binary
    binary_path = '/home/user/fast_query'
    assert os.path.isfile(binary_path), f"Missing compiled binary at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

    start_time = time.time()
    proc = subprocess.run([binary_path, str(start_node), str(end_node)], capture_output=True, text=True)
    end_time = time.time()

    assert proc.returncode == 0, f"fast_query failed with exit code {proc.returncode}. Stderr: {proc.stderr}"

    runtime = end_time - start_time
    assert runtime <= 0.5, f"Runtime {runtime:.4f}s exceeded threshold of 0.5s"