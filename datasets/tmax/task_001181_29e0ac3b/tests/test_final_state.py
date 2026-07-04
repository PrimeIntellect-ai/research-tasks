# test_final_state.py

import os
import requests
import pytest

def expected_simulation_result(graph_data):
    nodes = graph_data['nodes']
    edges = graph_data['edges']

    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    positions = [float(i) for i in range(len(nodes))]
    velocities = [0.0] * len(nodes)
    velocities[0] = 1.0

    history = []
    for _ in range(1000):
        forces = [0.0] * len(positions)
        for node in sorted(adj.keys()):
            for neighbor in sorted(adj[node]):
                forces[node] += (positions[neighbor] - positions[node]) * 0.1

        for i in range(len(nodes)):
            velocities[i] += forces[i] * 0.01
            positions[i] += velocities[i] * 0.01
        history.append(positions[0])

    crossings = 0
    for i in range(1, len(history)):
        if history[i-1] < 0 and history[i] >= 0:
            crossings += 1

    return crossings / 10.0

def test_reference_freq_file():
    path = "/home/user/reference_freq.txt"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "5.00", f"Expected '5.00' in {path}, got '{content}'"

def test_api_simulate_endpoint():
    url = "http://127.0.0.1:8080/simulate"

    payload = {
        "nodes": [0, 1, 2, 3, 4],
        "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Failed to parse JSON response: {response.text}")

    assert "dominant_frequency" in data, f"Key 'dominant_frequency' missing in response: {data}"

    expected_freq = expected_simulation_result(payload)
    actual_freq = data["dominant_frequency"]

    assert isinstance(actual_freq, (int, float)), "dominant_frequency must be a number"
    assert abs(actual_freq - expected_freq) < 1e-5, f"Expected dominant_frequency {expected_freq}, got {actual_freq}"