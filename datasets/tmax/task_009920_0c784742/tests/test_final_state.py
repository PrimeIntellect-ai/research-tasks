# test_final_state.py

import os
import json

def test_flagged_users_output():
    jsonl_path = "/home/user/graph_data.jsonl"
    output_path = "/home/user/flagged_users.txt"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist. The Go program must generate this file."
    assert os.path.exists(jsonl_path), f"Input file {jsonl_path} is missing."

    nodes = {}
    edges = []

    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("type") == "node":
                nodes[obj["id"]] = obj
            elif obj.get("type") == "edge":
                edges.append(obj)

    # Find the target resource ID
    target_res_ids = [
        n["id"] for n in nodes.values() 
        if n.get("label") == "Resource" and n.get("name") == "customer_pii_db"
    ]
    assert len(target_res_ids) == 1, "Could not uniquely identify the 'customer_pii_db' resource in the graph."
    target_res_id = target_res_ids[0]

    # Build reverse adjacency list to find all nodes that can reach the target resource
    # Edges:
    # User -[HAS_ROLE]-> Role
    # Role -[INHERITS]-> Role
    # Role -[CAN_ACCESS]-> Resource
    reverse_adj = {n: [] for n in nodes}
    for e in edges:
        if e["to"] in reverse_adj:
            reverse_adj[e["to"]].append((e["from"], e["relation"]))

    reachable_users = []
    visited = set()

    def dfs(current_id):
        if current_id in visited:
            return
        visited.add(current_id)

        node = nodes.get(current_id)
        if node and node.get("label") == "User":
            reachable_users.append(node)

        for neighbor, relation in reverse_adj.get(current_id, []):
            if relation in ("CAN_ACCESS", "INHERITS", "HAS_ROLE"):
                dfs(neighbor)

    dfs(target_res_id)

    # Sort users by ID as required
    reachable_users.sort(key=lambda u: u["id"])
    expected_lines = [f"{u['id']},{u['name']}" for u in reachable_users]

    # Read actual lines
    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {output_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )