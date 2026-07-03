# test_final_state.py

import os
import socket
import pytest
import random
from collections import deque

def get_graph():
    nodes = list(range(1, 201))
    edges = {n: [] for n in nodes}
    random.seed(42)
    for n in nodes:
        num_edges = random.randint(0, 5)
        edges[n] = random.sample(nodes, num_edges)
    return edges

def bfs(graph, start, end):
    if start == end:
        return [start]
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor in graph[node]:
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

def send_query(src, dst):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('127.0.0.1', 8888))
        msg = f"CHECK {src} {dst}\n"
        s.sendall(msg.encode('utf-8'))
        resp = s.recv(4096).decode('utf-8')
        return resp.strip()
    except Exception as e:
        pytest.fail(f"Failed to connect and query server for {src}->{dst}: {e}")
    finally:
        s.close()

def check_path(src, dst, response, graph):
    expected_path = bfs(graph, src, dst)
    if expected_path is None:
        assert response == "NONE", f"Expected 'NONE' for {src}->{dst}, got '{response}'"
        return

    assert response != "NONE", f"Expected a valid path for {src}->{dst}, got 'NONE'"

    try:
        path = [int(x.strip()) for x in response.split(',')]
    except ValueError:
        pytest.fail(f"Could not parse response as comma-separated integers: '{response}'")

    assert path[0] == src, f"Path must start with {src}, got {path[0]}"
    assert path[-1] == dst, f"Path must end with {dst}, got {path[-1]}"

    # Check shortest path length
    assert len(path) == len(expected_path), f"Expected shortest path of length {len(expected_path)}, but got length {len(path)}: {response}"

    # Check validity of edges
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        assert v in graph[u], f"Invalid edge in path: no direct access from {u} to {v}"

def test_server_binary_exists():
    binary_path = '/home/user/audit_server'
    assert os.path.isfile(binary_path), f"Server binary {binary_path} not found"
    assert os.access(binary_path, os.X_OK), f"Server binary {binary_path} is not executable"

def test_server_responses():
    graph = get_graph()

    # Pre-selected test cases to ensure coverage of connected, disconnected, and self-paths
    test_pairs = [
        (1, 50),
        (2, 100),
        (10, 10),
        (20, 199),
        (150, 3)
    ]

    # Add random pairs
    random.seed(1337)
    for _ in range(15):
        test_pairs.append((random.randint(1, 200), random.randint(1, 200)))

    for src, dst in test_pairs:
        resp = send_query(src, dst)
        check_path(src, dst, resp, graph)