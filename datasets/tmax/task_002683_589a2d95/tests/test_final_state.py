# test_final_state.py

import os
import csv
import time
import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"
NODES_CSV = "/home/user/data/nodes.csv"
EDGES_CSV = "/home/user/data/edges.csv"

def get_nodes():
    nodes = {}
    with open(NODES_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['node_id']] = row['node_type']
    return nodes

def get_edges():
    edges = []
    with open(EDGES_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append({
                'src': row['src_id'],
                'dst': row['dst_id'],
                'rel': row['relation_type']
            })
    return edges

def test_server_binary_exists():
    assert os.path.isfile("/home/user/graph_server"), "/home/user/graph_server binary does not exist."
    assert os.access("/home/user/graph_server", os.X_OK), "/home/user/graph_server is not executable."

def test_server_log_exists():
    log_path = "/home/user/server.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read()
    assert "SERVER READY" in content, f"'SERVER READY' not found in {log_path}."

def test_pattern_endpoint():
    nodes = get_nodes()
    edges = get_edges()

    # Expected matches for src_type=Person, dst_type=Company, rel=WorksFor
    expected_matches = []
    for e in edges:
        if e['rel'] == 'WorksFor':
            src_type = nodes.get(e['src'])
            dst_type = nodes.get(e['dst'])
            if src_type == 'Person' and dst_type == 'Company':
                expected_matches.append([e['src'], e['dst']])

    # Sort for comparison
    expected_matches.sort()

    try:
        response = requests.get(f"{BASE_URL}/pattern?src_type=Person&dst_type=Company&rel=WorksFor", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to pattern endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Response should be a JSON array"

    # Sort response for comparison
    actual_matches = sorted([list(match) for match in data])

    assert actual_matches == expected_matches, f"Pattern matches do not match expected. Expected {len(expected_matches)} matches."

def test_influence_endpoint():
    edges = get_edges()

    # Test a specific node
    test_node = "105"

    in_degree = sum(1 for e in edges if e['dst'] == test_node)
    out_degree = sum(1 for e in edges if e['src'] == test_node)
    expected_score = (in_degree * 3) + (out_degree * 2)

    try:
        response = requests.get(f"{BASE_URL}/influence?node={test_node}", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to influence endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, dict), "Response should be a JSON object"
    assert "node" in data, "Response missing 'node' key"
    assert "score" in data, "Response missing 'score' key"

    assert str(data["node"]) == test_node, f"Expected node {test_node}, got {data['node']}"
    assert data["score"] == expected_score, f"Expected score {expected_score}, got {data['score']}"