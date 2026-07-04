# test_final_state.py

import os
import json
import pytest
import requests
from collections import defaultdict

GROUND_TRUTH_PATH = "/app/services/ground_truth.json"
BASE_URL = "http://127.0.0.1:8080"

@pytest.fixture(scope="module")
def graph_data():
    assert os.path.isfile(GROUND_TRUTH_PATH), f"Ground truth file missing at {GROUND_TRUTH_PATH}"
    with open(GROUND_TRUTH_PATH, "r") as f:
        data = json.load(f)

    nodes = {node["id"]: node["type"] for node in data["nodes"]}
    adj = defaultdict(set)
    for edge in data["edges"]:
        # Handle both list [u, v] and dict {"source": u, "target": v} formats just in case
        if isinstance(edge, list):
            u, v = edge[0], edge[1]
        else:
            u, v = edge["source"], edge["target"]
        adj[u].add(v)
        adj[v].add(u)

    # Compute component sizes
    visited = set()
    component_sizes = {}
    for node in nodes:
        if node not in visited:
            comp = set()
            stack = [node]
            while stack:
                curr = stack.pop()
                if curr not in comp:
                    comp.add(curr)
                    stack.extend(adj[curr] - comp)
            for n in comp:
                component_sizes[n] = len(comp)
            visited.update(comp)

    return {
        "nodes": nodes,
        "adj": adj,
        "component_sizes": component_sizes
    }

def test_server_running():
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
    except requests.exceptions.RequestException:
        pytest.fail(f"Could not connect to the C++ server at {BASE_URL}. Is it running?")

def test_degree_endpoint(graph_data):
    test_nodes = list(graph_data["nodes"].keys())[:5]
    for node_id in test_nodes:
        expected_degree = len(graph_data["adj"][node_id])
        url = f"{BASE_URL}/analytics/degree?node={node_id}"
        try:
            resp = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")

        assert resp.status_code == 200, f"Expected status 200 for {url}, got {resp.status_code}"
        data = resp.json()
        assert "node" in data and data["node"] == node_id, f"Invalid node ID in response: {data}"
        assert "degree" in data and data["degree"] == expected_degree, f"Expected degree {expected_degree} for node {node_id}, got {data.get('degree')}"

def test_component_size_endpoint(graph_data):
    test_nodes = list(graph_data["nodes"].keys())[:5]
    for node_id in test_nodes:
        expected_size = graph_data["component_sizes"][node_id]
        url = f"{BASE_URL}/analytics/component_size?node={node_id}"
        try:
            resp = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")

        assert resp.status_code == 200, f"Expected status 200 for {url}, got {resp.status_code}"
        data = resp.json()
        assert "node" in data and data["node"] == node_id, f"Invalid node ID in response: {data}"
        assert "component_size" in data and data["component_size"] == expected_size, f"Expected component size {expected_size} for node {node_id}, got {data.get('component_size')}"

def test_query_endpoint(graph_data):
    # Find a node with neighbors of a specific type to test
    test_cases = []
    for node_id, neighbors in graph_data["adj"].items():
        if not neighbors:
            continue
        for target_type in ["Dataset", "Paper", "Author"]:
            matches = sorted([n for n in neighbors if graph_data["nodes"][n] == target_type])
            if matches:
                test_cases.append((node_id, target_type, matches))
                break
        if len(test_cases) >= 3:
            break

    if not test_cases:
        # Fallback if graph is empty or disconnected
        test_cases = [(10, "Paper", [])]

    for node_id, target_type, expected_results in test_cases:
        query_str = f"MATCH (a)-[]-(b) WHERE a.id = {node_id} AND b.type = '{target_type}' RETURN b.id"
        payload = {"query": query_str}
        url = f"{BASE_URL}/query"

        try:
            resp = requests.post(url, json=payload, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"POST request to {url} failed: {e}")

        assert resp.status_code == 200, f"Expected status 200 for {url}, got {resp.status_code}"
        data = resp.json()
        assert "results" in data, f"Missing 'results' key in response: {data}"
        assert data["results"] == expected_results, f"Expected results {expected_results} for query '{query_str}', got {data['results']}"