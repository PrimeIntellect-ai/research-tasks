# test_final_state.py

import os
import sqlite3
import pytest
import requests
import time

DB_PATH = "/app/knowledge.db"
BASE_URL = "http://127.0.0.1:8080"

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just check if the port is open and responding to HTTP
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if index idx_edge_opt exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edge_opt'")
    index = cursor.fetchone()
    assert index is not None, "Index 'idx_edge_opt' was not created in the database."

    # Optionally check the columns of the index
    cursor.execute("PRAGMA index_info(idx_edge_opt)")
    columns = [row[2] for row in cursor.fetchall()]
    assert "source_node" in columns and "edge_label" in columns, "Index 'idx_edge_opt' does not cover the required columns (source_node, edge_label)."

    conn.close()

def test_api_traverse_knows_depth_2():
    # Ensure server is up
    assert wait_for_server(f"{BASE_URL}/api/traverse?start_node=N1&edge_label=KNOWS&max_depth=1"), "HTTP server is not reachable on 127.0.0.1:8080"

    url = f"{BASE_URL}/api/traverse"
    params = {
        "start_node": "N1",
        "edge_label": "KNOWS",
        "max_depth": 2
    }
    response = requests.get(url, params=params, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "reachable_nodes" in data, "Response JSON missing 'reachable_nodes' key"
    assert "count" in data, "Response JSON missing 'count' key"

    expected_nodes = ["N2", "N3"]
    assert data["reachable_nodes"] == expected_nodes, f"Expected reachable_nodes {expected_nodes}, got {data['reachable_nodes']}"
    assert data["count"] == len(expected_nodes), f"Expected count {len(expected_nodes)}, got {data['count']}"

def test_api_traverse_likes_depth_1():
    url = f"{BASE_URL}/api/traverse"
    params = {
        "start_node": "N1",
        "edge_label": "LIKES",
        "max_depth": 1
    }
    response = requests.get(url, params=params, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()

    expected_nodes = ["N7"]
    assert data["reachable_nodes"] == expected_nodes, f"Expected reachable_nodes {expected_nodes}, got {data['reachable_nodes']}"
    assert data["count"] == len(expected_nodes), f"Expected count {len(expected_nodes)}, got {data['count']}"

def test_api_traverse_filters_deleted():
    # N1 to N5 is deleted. N5 to N6 is not deleted.
    # Traversing N1 KNOWS depth 3 should not reach N5 or N6.
    url = f"{BASE_URL}/api/traverse"
    params = {
        "start_node": "N1",
        "edge_label": "KNOWS",
        "max_depth": 3
    }
    response = requests.get(url, params=params, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()

    expected_nodes = ["N2", "N3", "N4"]
    assert data["reachable_nodes"] == expected_nodes, f"Expected reachable_nodes {expected_nodes}, got {data['reachable_nodes']} (Make sure deleted edges are filtered out)"
    assert data["count"] == len(expected_nodes), f"Expected count {len(expected_nodes)}, got {data['count']}"