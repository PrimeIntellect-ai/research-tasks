# test_final_state.py
import os
import json
import requests
import pytest

URL = "http://127.0.0.1:9000/build-order"
TOKEN = "DELTA-NINER-WHISKEY-TWO"
GRAPH_PATH = "/home/user/mobile_graph.json"

def compute_expected_order(graph):
    # Calculate in-degrees
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            if v not in in_degree:
                in_degree[v] = 0
            in_degree[u] += 1

    # Add nodes not explicitly in keys but present in values
    for u in list(in_degree.keys()):
        if u not in graph:
            graph[u] = []

    # Initialize priority queue (using sorted list for simplicity)
    queue = [u for u in in_degree if in_degree[u] == 0]
    queue.sort()

    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        # For topological sort, we need to find nodes that depend on u
        # The graph maps Node -> Dependencies
        # So if we built u, we satisfy one dependency for nodes that depend on u
        for node, deps in graph.items():
            if u in deps:
                in_degree[node] -= 1
                if in_degree[node] == 0:
                    queue.append(node)
                    queue.sort()

    return order

def test_server_running_and_unauthorized_no_token():
    try:
        response = requests.get(URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server is not running or unreachable at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when no token is provided, got {response.status_code}"

def test_unauthorized_wrong_token():
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    try:
        response = requests.get(URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server is not running or unreachable at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when wrong token is provided, got {response.status_code}"

def test_authorized_correct_response():
    assert os.path.isfile(GRAPH_PATH), f"Graph file missing at {GRAPH_PATH}"
    with open(GRAPH_PATH, 'r') as f:
        graph = json.load(f)

    expected_order = compute_expected_order(graph)

    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server is not running or unreachable at {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}"

    try:
        actual_order = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert actual_order == expected_order, f"Expected build order {expected_order}, but got {actual_order}"