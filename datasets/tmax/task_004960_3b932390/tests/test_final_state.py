# test_final_state.py

import os
import sys
import time
import json
import sqlite3
import random
import heapq
from collections import defaultdict
import pytest

try:
    import cv2
    from pyzbar.pyzbar import decode
except ImportError:
    pass  # We'll assume they are available in the runtime if the hint suggested them.

DB_PATH = "/home/user/etl_graph.db"
ANALYZE_SCRIPT = "/home/user/analyze.py"
VIDEO_PATH = "/app/etl_monitor.mp4"

def extract_truth_data():
    """Extract truth edges from the video using pyzbar."""
    cap = cv2.VideoCapture(VIDEO_PATH)
    edges = []
    seen = set()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            if data not in seen:
                seen.add(data)
                edges.append(json.loads(data))
    cap.release()
    return edges

def get_truth_deadlocks(edges):
    """Compute the expected deadlocks from truth data."""
    graphs = defaultdict(list)
    for e in edges:
        graphs[e['tx_id']].append((e['source'], e['target']))

    deadlocks = []
    for tx_id, edge_list in graphs.items():
        adj = defaultdict(list)
        for u, v in edge_list:
            adj[u].append(v)

        visited = set()
        rec_stack = set()

        def is_cyclic(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    if is_cyclic(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        has_cycle = False
        for node in list(adj.keys()):
            if node not in visited:
                if is_cyclic(node):
                    has_cycle = True
                    break
        if has_cycle:
            deadlocks.append(tx_id)

    return sorted(deadlocks)

def get_truth_shortest_path_func(edges):
    """Return a function that computes the truth shortest path."""
    graphs = defaultdict(lambda: defaultdict(list))
    for e in edges:
        graphs[e['tx_id']][e['source']].append((e['target'], e['duration_ms']))

    def get_sp(tx_id, source, target):
        adj = graphs[tx_id]
        pq = [(0, source)]
        dist = {source: 0}
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float('inf')):
                continue
            if u == target:
                return d
            for v, weight in adj[u]:
                if dist.get(v, float('inf')) > d + weight:
                    dist[v] = d + weight
                    heapq.heappush(pq, (dist[v], v))
        return -1
    return get_sp, graphs

def test_analyze_script_exists():
    assert os.path.isfile(ANALYZE_SCRIPT), f"Missing script: {ANALYZE_SCRIPT}"
    assert os.path.isfile(DB_PATH), f"Missing database: {DB_PATH}"

def test_deadlocks_correctness():
    sys.path.insert(0, os.path.dirname(ANALYZE_SCRIPT))
    try:
        import analyze
    except ImportError as e:
        pytest.fail(f"Failed to import analyze.py: {e}")

    edges = extract_truth_data()
    expected_deadlocks = get_truth_deadlocks(edges)

    actual_deadlocks = analyze.find_deadlocks(DB_PATH)
    assert actual_deadlocks == expected_deadlocks, (
        f"Deadlocks mismatch. Expected {expected_deadlocks}, got {actual_deadlocks}"
    )

def test_shortest_path_benchmark():
    sys.path.insert(0, os.path.dirname(ANALYZE_SCRIPT))
    import analyze

    edges = extract_truth_data()
    truth_sp_func, graphs = get_truth_shortest_path_func(edges)

    # Generate 5000 valid query parameters
    queries = []
    # Collect all nodes per tx_id
    nodes_per_tx = defaultdict(list)
    for e in edges:
        nodes_per_tx[e['tx_id']].append(e['source'])
        nodes_per_tx[e['tx_id']].append(e['target'])

    for tx_id in nodes_per_tx:
        nodes_per_tx[tx_id] = list(set(nodes_per_tx[tx_id]))

    tx_ids = list(nodes_per_tx.keys())
    random.seed(42)
    for _ in range(5000):
        tx = random.choice(tx_ids)
        src = random.choice(nodes_per_tx[tx])
        tgt = random.choice(nodes_per_tx[tx])
        queries.append((tx, src, tgt))

    # Verify correctness on a subset
    for q in queries[:50]:
        expected = truth_sp_func(*q)
        actual = analyze.get_shortest_path_duration(DB_PATH, *q)
        assert actual == expected, f"Shortest path mismatch for {q}. Expected {expected}, got {actual}"

    # Benchmark
    start_time = time.time()
    for q in queries:
        analyze.get_shortest_path_duration(DB_PATH, *q)
    end_time = time.time()

    duration = end_time - start_time
    assert duration < 1.5, f"Benchmark failed: took {duration:.3f} seconds, expected < 1.5 seconds. Check your database indexing."