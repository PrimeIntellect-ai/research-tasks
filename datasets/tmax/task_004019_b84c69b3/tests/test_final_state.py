# test_final_state.py
import requests
import pytest
import time

def test_api_threats_endpoint():
    url = "http://127.0.0.1:8080/api/v1/threats"

    max_retries = 3
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException as e:
            if i < max_retries - 1:
                time.sleep(1)
            else:
                pytest.fail(f"Failed to connect to the API server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response text: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response text: {response.text}")

    assert data.get("status") == "success", f"Expected 'status' to be 'success', got {data.get('status')}"

    primary_edges = data.get("primary_malicious_edges", [])
    assert len(primary_edges) == 2, f"Expected 2 primary malicious edges, got {len(primary_edges)}"

    expected_edges = [
        {"src": "10.0.0.2", "dst": "10.0.0.3", "timestamp": 12.2},
        {"src": "192.168.1.10", "dst": "10.0.0.5", "timestamp": 25.4}
    ]

    for edge in expected_edges:
        assert edge in primary_edges, f"Expected edge {edge} not found in primary_malicious_edges. Actual edges: {primary_edges}"

    secondary_nodes = data.get("secondary_compromised_nodes", [])
    assert len(secondary_nodes) == 1, f"Expected 1 secondary compromised node, got {len(secondary_nodes)}"
    assert "10.0.0.4" in secondary_nodes, f"Expected '10.0.0.4' in secondary_compromised_nodes. Actual nodes: {secondary_nodes}"