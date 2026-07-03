# test_final_state.py

import os
import csv
import json
import time
import heapq
import subprocess
import pytest

def get_expected_path():
    graph = {}
    csv_path = '/home/user/data/edges.csv'
    assert os.path.exists(csv_path), f"Data file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row['source']
            v = row['target']
            w = int(row['weight'])
            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))

    start = "START_NODE"
    end = "END_NODE"

    pq = [(0, start)]
    distances = {start: 0}
    previous = {start: None}

    while pq:
        dist, current = heapq.heappop(pq)

        if current == end:
            break

        if dist > distances.get(current, float('inf')):
            continue

        for neighbor, weight in graph.get(current, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                previous[neighbor] = (current, weight)
                heapq.heappush(pq, (new_dist, neighbor))

    if end not in distances:
        pytest.fail(f"No path found from {start} to {end} in the dataset.")

    path = []
    curr = end
    while curr != start:
        prev, w = previous[curr]
        path.append((curr, w))
        curr = prev
    path.reverse()

    result = [{"node": start, "cumulative_weight": 0}]
    cum_weight = 0
    for node, w in path:
        cum_weight += w
        result.append({"node": node, "cumulative_weight": cum_weight})

    return result

def test_analyze_script_execution_and_output():
    script_path = "/home/user/analyze.go"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Remove result.json if it exists to ensure we are testing the new output
    result_file = "/home/user/result.json"
    if os.path.exists(result_file):
        os.remove(result_file)

    start_time = time.time()
    proc = subprocess.run(
        ["go", "run", "analyze.go"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    end_time = time.time()

    duration = end_time - start_time

    assert proc.returncode == 0, f"go run analyze.go failed with exit code {proc.returncode}.\nStderr: {proc.stderr}\nStdout: {proc.stdout}"
    assert duration < 1.0, f"Execution time {duration:.3f}s exceeded threshold of 1.0s. The graphdb package may not be properly optimized."

    assert os.path.exists(result_file), f"Output file {result_file} was not created."

    with open(result_file, "r") as f:
        try:
            actual_result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_file} is not valid JSON.")

    expected_result = get_expected_path()

    assert len(actual_result) == len(expected_result), f"Path length mismatch. Expected {len(expected_result)} nodes, got {len(actual_result)} nodes."

    for i, (actual, expected) in enumerate(zip(actual_result, expected_result)):
        assert actual.get("node") == expected["node"], f"Node mismatch at step {i}: expected {expected['node']}, got {actual.get('node')}."
        assert actual.get("cumulative_weight") == expected["cumulative_weight"], f"Cumulative weight mismatch at step {i} for node {expected['node']}: expected {expected['cumulative_weight']}, got {actual.get('cumulative_weight')}."