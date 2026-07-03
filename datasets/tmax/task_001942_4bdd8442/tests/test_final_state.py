# test_final_state.py

import pytest
import requests
import sqlite3
import subprocess
import heapq

BASE_URL = "http://127.0.0.1:9000"
AUTH_HEADER = {"Authorization": "Bearer ADMIN_TOKEN_99"}
DB_PATH = "/home/user/network.db"
ORACLE_PATH = "/app/link_cost_oracle"

def get_oracle_cost(src: int, dst: int) -> int:
    result = subprocess.run(
        [ORACLE_PATH, str(src), str(dst)],
        capture_output=True,
        text=True,
        check=True
    )
    return int(result.stdout.strip())

def compute_shortest_path(start: int, end: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT source_id, target_id FROM links")
    links = cursor.fetchall()
    conn.close()

    # Build adjacency list
    graph = {}
    for u, v in links:
        if u not in graph: graph[u] = []
        graph[u].append(v)
        # Note: the problem says "traverse the graph defined by the links table". 
        # Usually links are directed unless specified. Let's assume directed as per source/target, 
        # but if it's undirected, we might need both. The problem says "from source_id to target_id".
        # We will treat it as directed based on source_id -> target_id.

    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, current, path = heapq.heappop(pq)

        if current == end:
            return path, cost

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                edge_cost = get_oracle_cost(current, neighbor)
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))

    return None, None

def test_auth_missing():
    response = requests.get(f"{BASE_URL}/routers?tier=edge&limit=1&offset=0")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_auth_invalid():
    response = requests.get(f"{BASE_URL}/routers?tier=edge&limit=1&offset=0", headers={"Authorization": "Bearer WRONG_TOKEN"})
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_routers_endpoint():
    # tier=edge, routers are 5 and 6. Sorted descending: 6, 5.
    # limit=1, offset=1 should return 5.
    response = requests.get(f"{BASE_URL}/routers?tier=edge&limit=1&offset=1", headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.json()
    assert "data" in data, "Response missing 'data' key"
    assert len(data["data"]) == 1, "Expected exactly 1 router in data"

    router = data["data"][0]
    assert router["id"] == 5, f"Expected router ID 5, got {router.get('id')}"
    assert router["name"] == "edge-1", f"Expected router name 'edge-1', got {router.get('name')}"
    assert router["tier"] == "edge", f"Expected router tier 'edge', got {router.get('tier')}"

def test_route_endpoint_success():
    start_id = 1
    end_id = 6
    expected_path, expected_cost = compute_shortest_path(start_id, end_id)
    assert expected_path is not None, "Test setup error: no path exists in DB"

    response = requests.get(f"{BASE_URL}/route?start={start_id}&end={end_id}", headers=AUTH_HEADER)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    data = response.json()
    assert "path" in data, "Response missing 'path' key"
    assert "total_cost" in data, "Response missing 'total_cost' key"

    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"
    assert data["total_cost"] == expected_cost, f"Expected cost {expected_cost}, got {data['total_cost']}"

def test_route_endpoint_not_found():
    response = requests.get(f"{BASE_URL}/route?start=1&end=999", headers=AUTH_HEADER)
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"

    data = response.json()
    assert "error" in data, "Response missing 'error' key"