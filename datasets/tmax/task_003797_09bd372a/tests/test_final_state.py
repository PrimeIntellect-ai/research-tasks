# test_final_state.py

import os
import re
import heapq

def test_files_exist():
    """Verify that the required files have been created."""
    assert os.path.isfile("/home/user/graph_db/fast_query.cpp"), "/home/user/graph_db/fast_query.cpp is missing. Did you write the C++ program?"
    assert os.path.isfile("/home/user/graph_db/fast_query"), "/home/user/graph_db/fast_query is missing. Did you compile the C++ program?"
    assert os.path.isfile("/home/user/graph_db/result.log"), "/home/user/graph_db/result.log is missing. Did you run the program and redirect output?"

def test_result_log_correctness():
    """Verify that the result.log contains the correct minimum cost and a valid path."""
    edges_file = "/home/user/graph_db/edges.csv"
    assert os.path.isfile(edges_file), "edges.csv is missing. The data file must not be deleted."

    # Parse edges into a graph representation
    graph = {}
    with open(edges_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 3:
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                if u not in graph:
                    graph[u] = {}
                # In case of multiple edges between the same nodes, keep the minimum cost
                if v not in graph[u] or w < graph[u][v]:
                    graph[u][v] = w

    # Compute the expected shortest path cost using Dijkstra's algorithm
    dist = {10: 0}
    pq = [(0, 10)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == 500:
            break
        for v, w in graph.get(u, {}).items():
            if dist.get(v, float('inf')) > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))

    expected_cost = dist.get(500, float('inf'))
    assert expected_cost != float('inf'), "No path found in edges.csv from 10 to 500."

    # Read and parse result.log
    with open("/home/user/graph_db/result.log", "r") as f:
        content = f.read()

    cost_match = re.search(r"Cost:\s*(\d+)", content)
    assert cost_match, "Could not find a valid 'Cost: [TOTAL_COST]' line in result.log."
    reported_cost = int(cost_match.group(1))

    path_match = re.search(r"Path:\s*([\d\s->]+)", content)
    assert path_match, "Could not find a valid 'Path: 10 -> ... -> 500' line in result.log."

    path_str = path_match.group(1).strip()
    path_nodes = [int(x.strip()) for x in path_str.split("->") if x.strip().isdigit()]

    assert reported_cost == expected_cost, f"Reported cost {reported_cost} does not match the actual minimum cost {expected_cost}."
    assert len(path_nodes) >= 2, "Path must contain at least two nodes."
    assert path_nodes[0] == 10, f"Path starts at {path_nodes[0]}, expected 10."
    assert path_nodes[-1] == 500, f"Path ends at {path_nodes[-1]}, expected 500."

    # Verify that the reported path is valid and its cost sums up to the expected cost
    actual_path_cost = 0
    for i in range(len(path_nodes) - 1):
        u, v = path_nodes[i], path_nodes[i+1]
        assert u in graph and v in graph[u], f"Invalid transition in path: Edge {u} -> {v} does not exist in edges.csv."
        actual_path_cost += graph[u][v]

    assert actual_path_cost == expected_cost, f"The sum of edge costs in the reported path ({actual_path_cost}) does not match the expected minimum cost ({expected_cost}). The path is not optimal."