# test_final_state.py

import pytest
import requests
import time

def wait_for_server(url, timeout=5):
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code in (200, 404, 400):
                return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

def test_server_running_and_responds():
    """Test that the server is running on 127.0.0.1:8000 and responds to requests."""
    base_url = "http://127.0.0.1:8000"
    assert wait_for_server(base_url), f"Server is not reachable at {base_url} within the timeout period."

@pytest.mark.parametrize("node_id", [101, 103, 104])
def test_centrality_active_nodes(node_id):
    """Test that the centrality for active nodes is correctly computed as roughly 1/3."""
    url = f"http://127.0.0.1:8000/api/centrality?node={node_id}"

    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for node {node_id}, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "node" in data, f"Key 'node' missing in response for node {node_id}. Got: {data}"
    assert "centrality" in data, f"Key 'centrality' missing in response for node {node_id}. Got: {data}"

    assert int(data["node"]) == node_id, f"Expected node {node_id}, but got {data['node']}"

    centrality = float(data["centrality"])
    # The graph is a perfect cycle of 3 nodes: 101 -> 103 -> 104 -> 101.
    # PageRank for a perfect cycle should be exactly 1/N for each node, where N=3.
    # Thus, centrality should be approximately 0.3333.
    expected_centrality = 1.0 / 3.0
    assert abs(centrality - expected_centrality) < 0.02, f"Expected centrality for node {node_id} to be near {expected_centrality}, but got {centrality}"