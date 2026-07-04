# test_final_state.py
import os
import json
import time
import pytest
import requests
import threading

def test_processed_graph_exists_and_correct():
    path = "/home/user/processed_graph.json"
    assert os.path.isfile(path), f"Processed graph file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "nodes" in data, "Processed graph missing 'nodes' key."
    assert "edges" in data, "Processed graph missing 'edges' key."

    # Verify nodes
    node_ids = {n.get("id") for n in data["nodes"]}
    assert {1, 2, 3, 4}.issubset(node_ids), "Missing expected node IDs in processed graph."

    # Verify edges and weights
    edges_map = {(e.get("source"), e.get("target")): e.get("weight") for e in data["edges"]}

    # Expected weights based on window function: raw_collaborations / MAX(raw_collaborations) OVER (PARTITION BY source_id)
    # 1->2: 10 / max(10, 5) = 1.0
    # 1->3: 5 / max(10, 5) = 0.5
    # 2->4: 20 / 20 = 1.0
    # 3->4: 10 / 10 = 1.0
    expected_edges = {
        (1, 2): 1.0,
        (1, 3): 0.5,
        (2, 4): 1.0,
        (3, 4): 1.0
    }

    for edge, expected_weight in expected_edges.items():
        assert edge in edges_map, f"Edge {edge} missing in processed graph."
        assert abs(edges_map[edge] - expected_weight) < 1e-6, f"Edge {edge} has incorrect weight. Expected {expected_weight}, got {edges_map[edge]}."

def test_api_server_shortest_path():
    url = "http://127.0.0.1:8080/shortest_path?src=1&dst=4"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "path" in data, "Response missing 'path' key."
    assert "total_weight" in data, "Response missing 'total_weight' key."

    # Shortest path is 1 -> 3 -> 4 with weight 1.5
    assert data["path"] == [1, 3, 4] or data["path"] == ["1", "3", "4"], f"Incorrect shortest path. Expected [1, 3, 4], got {data['path']}."
    assert abs(float(data["total_weight"]) - 1.5) < 1e-6, f"Incorrect total weight. Expected 1.5, got {data['total_weight']}."

def test_api_server_concurrent_updates_no_deadlock():
    # Test for deadlock fix in vendored library
    url = "http://127.0.0.1:8080/update_edge"

    def update_edge(src, dst, weight, results, index):
        try:
            resp = requests.post(url, json={"source": src, "target": dst, "weight": weight}, timeout=5)
            results[index] = resp.status_code
        except Exception as e:
            results[index] = str(e)

    results = [None, None]

    t1 = threading.Thread(target=update_edge, args=(1, 2, 2.0, results, 0))
    t2 = threading.Thread(target=update_edge, args=(2, 1, 3.0, results, 1))

    start_time = time.time()
    t1.start()
    t2.start()

    t1.join(timeout=5)
    t2.join(timeout=5)

    duration = time.time() - start_time

    assert t1.is_alive() is False and t2.is_alive() is False, "Concurrent requests deadlocked or timed out."
    assert results[0] == 200, f"Request 1 failed: {results[0]}"
    assert results[1] == 200, f"Request 2 failed: {results[1]}"
    assert duration < 5, f"Concurrent requests took too long ({duration}s), indicating potential deadlock or timeout."