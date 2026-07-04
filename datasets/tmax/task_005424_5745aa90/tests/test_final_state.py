# test_final_state.py
import os
import json
import pytest

def get_edges():
    edges = []
    with open("/home/user/data/edges.csv", "r") as f:
        lines = f.read().strip().splitlines()
        for line in lines[1:]:
            u, v, w = line.split(",")
            edges.append((u, v, float(w)))
    return edges

def get_wcc(edges):
    adj = {}
    for u, v, _ in edges:
        if u not in adj: adj[u] = set()
        if v not in adj: adj[v] = set()
        adj[u].add(v)
        adj[v].add(u)

    visited = set()
    components = []
    for node in adj:
        if node not in visited:
            comp = set()
            queue = [node]
            visited.add(node)
            while queue:
                curr = queue.pop(0)
                comp.add(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(comp)
    return components

def calculate_pagerank(edges, alpha=0.85, max_iter=100, tol=1.0e-6):
    nodes = set()
    out_weights = {}
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
        if u not in out_weights:
            out_weights[u] = 0.0
        out_weights[u] += w

    N = len(nodes)
    pr = {n: 1.0 / N for n in nodes}

    for _ in range(max_iter):
        new_pr = {n: 0.0 for n in nodes}
        dangling_sum = 0.0
        for n in nodes:
            if out_weights.get(n, 0) == 0:
                dangling_sum += pr[n]

        for n in nodes:
            new_pr[n] = (1.0 - alpha) / N + alpha * dangling_sum / N

        for u, v, w in edges:
            new_pr[v] += alpha * pr[u] * (w / out_weights[u])

        err = sum(abs(new_pr[n] - pr[n]) for n in nodes)
        pr = new_pr
        if err < tol:
            break
    return pr

def test_output_file_exists():
    assert os.path.exists("/home/user/output/nodes.jsonl"), "Output file /home/user/output/nodes.jsonl is missing"

def test_output_content():
    edges = get_edges()
    components = get_wcc(edges)
    pr = calculate_pagerank(edges)

    expected_nodes = {}
    for comp in components:
        if len(comp) >= 3:
            for node in comp:
                expected_nodes[node] = {
                    "node_id": node,
                    "pagerank": pr[node],
                    "component_size": len(comp)
                }

    expected_sorted_keys = sorted(expected_nodes.keys())

    actual = []
    with open("/home/user/output/nodes.jsonl", "r") as f:
        for line in f:
            if line.strip():
                actual.append(json.loads(line))

    assert len(actual) == len(expected_sorted_keys), f"Expected {len(expected_sorted_keys)} records, got {len(actual)}"

    for i, act in enumerate(actual):
        exp_key = expected_sorted_keys[i]
        exp = expected_nodes[exp_key]

        assert act.get("node_id") == exp["node_id"], f"Record {i} node_id mismatch. Expected {exp['node_id']}, got {act.get('node_id')}"
        assert act.get("component_size") == exp["component_size"], f"Record {i} component_size mismatch. Expected {exp['component_size']}, got {act.get('component_size')}"

        act_pr = act.get("pagerank")
        assert isinstance(act_pr, float), f"Record {i} pagerank should be a float, got {type(act_pr)}"
        assert abs(act_pr - exp["pagerank"]) < 1e-4, f"Record {i} pagerank mismatch. Expected ~{exp['pagerank']}, got {act_pr}"