# test_final_state.py
import os
import json
import pytest
from collections import defaultdict, deque

def compute_expected_solution(raw_data_path):
    with open(raw_data_path, 'r') as f:
        data = json.load(f)

    # Filter and aggregate
    edges = defaultdict(int)
    for tx in data:
        if tx.get("amount", 0) >= 1000:
            edge = (tx["from_acct"], tx["to_acct"])
            edges[edge] += tx["amount"]

    if not edges:
        return None

    # Find top edge overall
    top_edge = max(edges.items(), key=lambda x: x[1])
    top_edge_dict = {
        "from_acct": top_edge[0][0],
        "to_acct": top_edge[0][1],
        "total_volume": top_edge[1]
    }

    # Build graph for BFS
    graph = defaultdict(list)
    for (u, v) in edges.keys():
        graph[u].append(v)

    # BFS for shortest path (fewest hops)
    start = "ACCT_START"
    target = "ACCT_TARGET"
    queue = deque([[start]])
    visited = set([start])

    shortest_path = None
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            shortest_path = path
            break

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    if not shortest_path:
        return None

    # Compute path volume sum
    path_volume_sum = 0
    for i in range(len(shortest_path) - 1):
        u = shortest_path[i]
        v = shortest_path[i+1]
        path_volume_sum += edges[(u, v)]

    return {
        "path": shortest_path,
        "path_volume_sum": path_volume_sum,
        "top_edge_overall": top_edge_dict
    }

def test_solution_file_exists():
    assert os.path.exists('/home/user/solution.json'), "The file /home/user/solution.json is missing."
    assert os.path.isfile('/home/user/solution.json'), "/home/user/solution.json is not a file."

def test_solution_content():
    raw_path = '/home/user/raw_transactions.json'
    assert os.path.exists(raw_path), f"Raw transactions file missing at {raw_path}."

    expected = compute_expected_solution(raw_path)
    assert expected is not None, "Could not compute expected solution from raw data."

    with open('/home/user/solution.json', 'r') as f:
        try:
            solution = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/solution.json does not contain valid JSON.")

    assert "path" in solution, "Missing 'path' in solution.json"
    assert solution["path"] == expected["path"], f"Expected path {expected['path']}, got {solution['path']}"

    assert "path_volume_sum" in solution, "Missing 'path_volume_sum' in solution.json"
    assert solution["path_volume_sum"] == expected["path_volume_sum"], f"Expected path_volume_sum {expected['path_volume_sum']}, got {solution['path_volume_sum']}"

    assert "top_edge_overall" in solution, "Missing 'top_edge_overall' in solution.json"
    top_edge = solution["top_edge_overall"]
    expected_top = expected["top_edge_overall"]
    assert top_edge.get("from_acct") == expected_top["from_acct"], f"Expected top edge from_acct {expected_top['from_acct']}, got {top_edge.get('from_acct')}"
    assert top_edge.get("to_acct") == expected_top["to_acct"], f"Expected top edge to_acct {expected_top['to_acct']}, got {top_edge.get('to_acct')}"
    assert top_edge.get("total_volume") == expected_top["total_volume"], f"Expected top edge total_volume {expected_top['total_volume']}, got {top_edge.get('total_volume')}"