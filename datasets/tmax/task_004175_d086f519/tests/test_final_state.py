# test_final_state.py

import os
import json
import sqlite3
import re
from collections import defaultdict
import pytest

DB_PATH = "/home/user/api_db.sqlite"
OUTPUT_PATH = "/home/user/migrated_api.json"

def translate_condition(condition):
    # Replace param.X and header.X
    condition = re.sub(r'\bparam\.([a-zA-Z0-9_]+)', r'req.param.\1', condition)
    condition = re.sub(r'\bheader\.([a-zA-Z0-9_]+)', r'req.header.\1', condition)
    # Replace operators
    condition = condition.replace(' = ', ' === ')
    condition = condition.replace(' != ', ' !== ')
    condition = condition.replace(' AND ', ' && ')
    condition = condition.replace(' OR ', ' || ')
    return f"req => {condition}"

def get_expected_json():
    # Read the initial database state to compute the expected output
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, path, condition FROM routes")
    routes = {row[0]: {"id": row[0], "path": row[1], "condition": row[2]} for row in cursor.fetchall()}

    cursor.execute("SELECT route_id, depends_on_id FROM depends_on")
    edges = cursor.fetchall()
    conn.close()

    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    # Find cycles and break them
    # A cycle is a back-edge in DFS. Since we need to remove the minimum number of edges,
    # and for multiple edges we remove the one with highest route_id.
    # For the given simple graph, we can just find all edges involved in cycles.
    def find_cycles():
        cycles = []
        visited = set()
        path = []
        path_set = set()

        def dfs(node):
            visited.add(node)
            path.append(node)
            path_set.add(node)
            for neighbor in adj[node]:
                if neighbor in path_set:
                    idx = path.index(neighbor)
                    cycles.append(path[idx:] + [neighbor])
                elif neighbor not in visited:
                    dfs(neighbor)
            path.pop()
            path_set.remove(node)

        for node in list(routes.keys()):
            if node not in visited:
                dfs(node)
        return cycles

    cycles = find_cycles()
    # Break cycles by removing the edge (route_id, depends_on_id) with highest route_id
    removed_edges = set()
    for cycle in cycles:
        # cycle is like [1, 4, 3, 1] meaning 1 depends on 4, 4 depends on 3, 3 depends on 1
        # Edges in cycle:
        cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
        # Filter out already removed edges
        cycle_edges = [e for e in cycle_edges if e not in removed_edges]
        if not cycle_edges:
            continue
        # Find edge with highest route_id
        edge_to_remove = max(cycle_edges, key=lambda e: e[0])
        removed_edges.add(edge_to_remove)
        adj[edge_to_remove[0]].remove(edge_to_remove[1])

    # Topological sort (Kahn's algorithm)
    # depends_on_id must be evaluated before route_id
    # So edge direction for topo sort is depends_on_id -> route_id
    in_degree = {u: 0 for u in routes}
    out_adj = defaultdict(list)
    for u in routes:
        for v in adj[u]:
            # u depends on v => v must come before u
            out_adj[v].append(u)
            in_degree[u] += 1

    import heapq
    queue = []
    for u in routes:
        if in_degree[u] == 0:
            heapq.heappush(queue, u)

    topo_order = []
    while queue:
        u = heapq.heappop(queue)
        topo_order.append(u)
        for neighbor in out_adj[u]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(queue, neighbor)

    assert len(topo_order) == len(routes), "Topological sort failed, cycle still exists."

    expected_json = []
    for u in topo_order:
        route = routes[u]
        expected_json.append({
            "id": route["id"],
            "path": route["path"],
            "js_validator": translate_condition(route["condition"])
        })

    return expected_json

def test_migrated_api_json_exists():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file."

def test_migrated_api_json_content():
    with open(OUTPUT_PATH, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {OUTPUT_PATH} as JSON: {e}")

    assert isinstance(actual_json, list), "The JSON output must be a list of route objects."

    expected_json = get_expected_json()

    assert len(actual_json) == len(expected_json), f"Expected {len(expected_json)} routes, but got {len(actual_json)}."

    for i, (actual, expected) in enumerate(zip(actual_json, expected_json)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert actual.get("id") == expected["id"], f"Route at index {i} has incorrect id. Expected {expected['id']}, got {actual.get('id')}."
        assert actual.get("path") == expected["path"], f"Route at index {i} has incorrect path. Expected {expected['path']}, got {actual.get('path')}."
        assert actual.get("js_validator") == expected["js_validator"], f"Route at index {i} has incorrect js_validator. Expected {expected['js_validator']}, got {actual.get('js_validator')}."