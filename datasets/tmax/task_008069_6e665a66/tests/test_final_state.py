# test_final_state.py
import os
import json
import sqlite3
from collections import deque
import pytest

def get_truth_values():
    db_path = '/home/user/network.db'
    if not os.path.exists(db_path):
        pytest.fail(f"Database file {db_path} is missing, cannot compute truth.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get servers mapping
    cursor.execute('SELECT id, hostname FROM servers')
    servers = {row[0]: row[1] for row in cursor.fetchall()}
    server_ids = {v: k for k, v in servers.items()}

    start_hostname = 'Gateway-01'
    end_hostname = 'Database-Cluster'

    if start_hostname not in server_ids or end_hostname not in server_ids:
        pytest.fail("Required servers are missing from the database.")

    start_id = server_ids[start_hostname]
    end_id = server_ids[end_hostname]

    # Build adjacency list
    cursor.execute('SELECT source_id, target_id FROM connections')
    adj = {}
    for u, v in cursor.fetchall():
        adj.setdefault(u, []).append(v)

    # BFS for shortest path
    queue = deque([[start_id]])
    visited = {start_id}
    shortest_path_ids = None

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end_id:
            shortest_path_ids = path
            break

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    if not shortest_path_ids:
        pytest.fail("No path found between Gateway-01 and Database-Cluster.")

    shortest_path_hostnames = [servers[nid] for nid in shortest_path_ids]

    # Compute total traffic for the shortest path
    total_traffic = 0
    for i in range(len(shortest_path_ids) - 1):
        u = shortest_path_ids[i]
        v = shortest_path_ids[i + 1]
        cursor.execute('SELECT SUM(bytes_transferred) FROM traffic_logs WHERE conn_source = ? AND conn_target = ?', (u, v))
        result = cursor.fetchone()[0]
        if result is not None:
            total_traffic += result

    conn.close()
    return shortest_path_hostnames, total_traffic


def test_solution_json_exists_and_valid():
    solution_path = '/home/user/solution.json'
    assert os.path.exists(solution_path), f"The solution file {solution_path} does not exist."

    with open(solution_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {solution_path} does not contain valid JSON.")

    assert isinstance(data, dict), "The JSON file should contain a dictionary object."
    assert "shortest_path" in data, "The JSON file is missing the 'shortest_path' key."
    assert "total_traffic" in data, "The JSON file is missing the 'total_traffic' key."


def test_solution_values():
    solution_path = '/home/user/solution.json'
    assert os.path.exists(solution_path), f"The solution file {solution_path} does not exist."

    with open(solution_path, 'r') as f:
        data = json.load(f)

    expected_path, expected_traffic = get_truth_values()

    actual_path = data.get("shortest_path")
    actual_traffic = data.get("total_traffic")

    assert actual_path == expected_path, \
        f"Incorrect shortest path. Expected {expected_path}, but got {actual_path}."

    assert actual_traffic == expected_traffic, \
        f"Incorrect total traffic. Expected {expected_traffic}, but got {actual_traffic}."