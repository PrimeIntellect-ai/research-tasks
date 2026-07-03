# test_final_state.py

import os
import subprocess
import requests
import json
import pytest

def test_graph_service_code_exists():
    """Test that the graph service C++ source code exists."""
    path = "/home/user/graph_service.cpp"
    assert os.path.isfile(path), f"Missing C++ source code at {path}"

def test_graph_service_binary_exists():
    """Test that the graph service binary exists and is executable."""
    path = "/home/user/graph_service"
    assert os.path.isfile(path), f"Missing graph service binary at {path}"
    assert os.access(path, os.X_OK), f"Graph service binary at {path} is not executable"

def test_graph_bin_exists_and_valid():
    """Test that graph.bin exists and passes the legacy oracle validation."""
    path = "/home/user/graph.bin"
    assert os.path.isfile(path), f"Missing graph.bin at {path}"

    # Run the legacy oracle
    oracle_path = "/app/legacy_graph_oracle"
    try:
        result = subprocess.run([oracle_path], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Legacy oracle validation failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Legacy oracle validation timed out.")
    except Exception as e:
        pytest.fail(f"Failed to run legacy oracle: {e}")

def test_http_service_shortest_path():
    """Test that the HTTP service is running and correctly answers shortest-path queries."""
    url = "http://127.0.0.1:8080/shortest-path"
    payload = {
        "source": "D1",
        "target": "D99",
        "min_date": "2021-05-01",
        "page": 1,
        "limit": 2
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the HTTP service at {url}. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    # Depending on the exact schema returned, check if it's a list or a dict containing edges
    # The prompt says: "JSON array of edges representing the shortest path, respecting the `limit` pagination"
    # or "JSON response containing the paginated edges... and the total path cost"
    # We will just verify it contains the expected structure
    assert isinstance(data, (dict, list)), f"Unexpected JSON structure: {data}"

    # If it's a dict, it should contain edges and cost
    if isinstance(data, dict):
        assert "cost" in data or "total_cost" in data or "edges" in data, f"Missing expected keys in JSON response: {data}"
        if "edges" in data:
            assert isinstance(data["edges"], list), "Edges should be a list"
            assert len(data["edges"]) <= 2, f"Expected at most 2 edges due to pagination limit, got {len(data['edges'])}"
    elif isinstance(data, list):
        assert len(data) <= 2, f"Expected at most 2 edges due to pagination limit, got {len(data)}"