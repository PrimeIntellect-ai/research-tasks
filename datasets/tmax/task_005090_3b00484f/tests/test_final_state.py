# test_final_state.py

import os
import time
import requests
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8080"

def wait_for_server():
    """Wait for the FastAPI server to be up and running."""
    max_retries = 10
    for i in range(max_retries):
        try:
            # Just checking if the port is open and responding to HTTP
            # The root endpoint might not exist, but we can check if we get a response
            requests.get(BASE_URL, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_fastapi_app_exists():
    assert os.path.isfile("/app/main.py"), "The FastAPI app file /app/main.py does not exist."

def test_server_is_running():
    assert wait_for_server(), "FastAPI server is not reachable on localhost:8080."

def test_concurrent_inserts_and_aggregation():
    # We will insert 50 edges concurrently to test the deadlock fix
    edges = []
    # Create 50 requests: 10 for each source
    for i in range(10):
        edges.append({"src": "test_A", "dst": f"test_dst_{i}", "weight": 1})
        edges.append({"src": "test_B", "dst": f"test_dst_{i}", "weight": 2})
        edges.append({"src": "test_C", "dst": f"test_dst_{i}", "weight": 3})
        edges.append({"src": "test_D", "dst": f"test_dst_{i}", "weight": 4})
        edges.append({"src": "test_E", "dst": f"test_dst_{i}", "weight": 5})

    def post_edge(edge):
        resp = requests.post(f"{BASE_URL}/edge", json=edge, timeout=5)
        resp.raise_for_status()
        return resp.status_code

    # Run concurrent POST requests
    success_count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(post_edge, edge) for edge in edges]
        for future in as_completed(futures):
            try:
                status = future.result()
                if status in (200, 201):
                    success_count += 1
            except Exception as e:
                pytest.fail(f"Concurrent POST request failed or timed out: {e}. This likely indicates a deadlock in TinyDB.")

    assert success_count == 50, f"Expected 50 successful POST requests, got {success_count}."

    # Now test the aggregate endpoint
    resp = requests.get(f"{BASE_URL}/aggregate", timeout=5)
    resp.raise_for_status()
    data = resp.json()

    assert isinstance(data, list), "Aggregate response must be a JSON list."

    # Filter out only our test nodes in case the student left other data
    test_nodes_data = [item for item in data if str(item.get("node", "")).startswith("test_")]

    expected_degrees = {
        "test_E": 50,
        "test_D": 40,
        "test_C": 30,
        "test_B": 20,
        "test_A": 10
    }

    actual_degrees = {item["node"]: item["out_degree"] for item in test_nodes_data}

    for node, expected_weight in expected_degrees.items():
        assert actual_degrees.get(node) == expected_weight, f"Expected out_degree for {node} to be {expected_weight}, got {actual_degrees.get(node)}"

    # Verify sorting
    # Must be sorted by out_degree descending, then node alphabetically ascending
    sorted_test_data = sorted(test_nodes_data, key=lambda x: (-x["out_degree"], x["node"]))

    # Check if the returned list's relative order for test nodes matches the expected sorted order
    # We extract just the test nodes from the returned list to check their relative ordering
    returned_test_nodes = [item["node"] for item in test_nodes_data]
    expected_test_nodes = [item["node"] for item in sorted_test_data]

    assert returned_test_nodes == expected_test_nodes, "The aggregate results are not sorted correctly (out_degree DESC, node ASC)."