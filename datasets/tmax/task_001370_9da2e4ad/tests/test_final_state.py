# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8888"

def test_graph_centrality():
    """Verify the /graph/centrality endpoint returns the correct top node."""
    url = f"{BASE_URL}/graph/centrality"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "top_node" in data, "Response JSON missing 'top_node' key"
    assert data["top_node"] == "U3", f"Expected top_node 'U3', got '{data['top_node']}'"

def test_nosql_aggregate():
    """Verify the /nosql/aggregate endpoint returns the correct top sender volume."""
    url = f"{BASE_URL}/nosql/aggregate"
    payload = {"min_amount": 100}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "top_sender_volume" in data, "Response JSON missing 'top_sender_volume' key"
    assert data["top_sender_volume"] == 300, f"Expected top_sender_volume 300, got {data['top_sender_volume']}"