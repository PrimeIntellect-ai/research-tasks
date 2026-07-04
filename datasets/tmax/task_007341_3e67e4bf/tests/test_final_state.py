# test_final_state.py
import os
import heapq
from collections import defaultdict

def compute_expected_order(edges_file):
    adj = defaultdict(list)
    indegree = defaultdict(int)
    nodes = set()

    with open(edges_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # "A B" means A depends on B, so B must be loaded before A.
            # This forms a directed edge from B to A.
            u, v = map(int, line.split())
            adj[v].append(u)
            indegree[u] += 1
            nodes.add(u)
            nodes.add(v)

    queue = []
    for node in nodes:
        if indegree[node] == 0:
            heapq.heappush(queue, node)

    result = []
    while queue:
        curr = heapq.heappop(queue)
        result.append(curr)
        for neighbor in adj[curr]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(queue, neighbor)

    return result

def test_load_order_correctness():
    output_path = "/home/user/load_order.txt"
    edges_path = "/home/user/plugin_manager/edges.txt"

    assert os.path.exists(edges_path), f"Edges file {edges_path} is missing."
    assert os.path.exists(output_path), (
        f"{output_path} does not exist. The Rust program likely did not run, "
        "failed to compile, or failed to write the output file."
    )

    expected_order = compute_expected_order(edges_path)
    expected_str = " ".join(map(str, expected_order))

    with open(output_path, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, (
        f"The plugin load order in {output_path} is incorrect.\n"
        f"Expected: '{expected_str}'\n"
        f"Actual:   '{actual_str}'\n"
        "Ensure you are performing a topological sort and always picking the "
        "smallest available plugin ID when breaking ties."
    )