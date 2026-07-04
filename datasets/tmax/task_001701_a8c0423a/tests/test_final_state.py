# test_final_state.py

import os
import json
import sqlite3
import heapq
import math
import pytest

DB_PATH = "/home/user/backups.db"
JSON_PATH = "/home/user/routing_plan.json"

def get_db_connection():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    return sqlite3.connect(DB_PATH)

def compute_expected_routing_plan():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read datacenters
    cursor.execute("SELECT id, name FROM datacenters")
    datacenters = {row[0]: row[1] for row in cursor.fetchall()}

    # Find IDs for Alpha and Omega
    alpha_id = next((k for k, v in datacenters.items() if v == 'DC-Alpha'), None)
    omega_id = next((k for k, v in datacenters.items() if v == 'DC-Omega'), None)

    assert alpha_id is not None, "DC-Alpha not found in database"
    assert omega_id is not None, "DC-Omega not found in database"

    # Read network links
    cursor.execute("SELECT source_id, dest_id, latency_ms FROM network_links")
    links = cursor.fetchall()

    # Build graph
    graph = {k: {} for k in datacenters.keys()}
    for u, v, w in links:
        graph[u][v] = w

    # Dijkstra's algorithm
    pq = [(0, alpha_id, [])]
    visited = set()
    shortest_path = None

    while pq:
        dist, current_node, path = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        path = path + [current_node]

        if current_node == omega_id:
            shortest_path = path
            break

        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path))

    assert shortest_path is not None, "No path found from DC-Alpha to DC-Omega"

    # Compute average speeds
    expected_plan = []
    for i in range(len(shortest_path) - 1):
        u = shortest_path[i]
        v = shortest_path[i+1]

        cursor.execute("""
            SELECT bytes_transferred, duration_ms 
            FROM transfer_logs 
            WHERE source_id = ? AND dest_id = ? AND status = 'SUCCESS'
            ORDER BY timestamp DESC 
            LIMIT 3
        """, (u, v))

        logs = cursor.fetchall()
        if not logs:
            avg_speed = 0.0
        else:
            speeds = [bytes_ / duration for bytes_, duration in logs]
            avg_speed = sum(speeds) / len(speeds)

        expected_plan.append({
            "source": datacenters[u],
            "dest": datacenters[v],
            "avg_speed_bytes_per_ms": round(avg_speed, 2)
        })

    conn.close()
    return expected_plan

def test_routing_plan_exists():
    assert os.path.exists(JSON_PATH), f"Routing plan file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file."

def test_routing_plan_format_and_correctness():
    assert os.path.exists(JSON_PATH), f"Routing plan file {JSON_PATH} does not exist."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_PATH} as JSON: {e}")

    assert isinstance(data, list), "JSON output must be a list of objects."

    expected_plan = compute_expected_routing_plan()

    assert len(data) == len(expected_plan), f"Expected {len(expected_plan)} hops in the routing plan, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_plan)):
        assert isinstance(actual, dict), f"Hop {i} is not a JSON object."

        # Check keys
        expected_keys = {"source", "dest", "avg_speed_bytes_per_ms"}
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Hop {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual["source"] == expected["source"], f"Hop {i} source mismatch. Expected '{expected['source']}', got '{actual['source']}'."
        assert actual["dest"] == expected["dest"], f"Hop {i} dest mismatch. Expected '{expected['dest']}', got '{actual['dest']}'."

        actual_speed = actual["avg_speed_bytes_per_ms"]
        expected_speed = expected["avg_speed_bytes_per_ms"]

        assert isinstance(actual_speed, (int, float)), f"Hop {i} avg_speed_bytes_per_ms must be a number."
        assert math.isclose(actual_speed, expected_speed, rel_tol=1e-5, abs_tol=1e-2), \
            f"Hop {i} avg_speed_bytes_per_ms mismatch. Expected {expected_speed}, got {actual_speed}."