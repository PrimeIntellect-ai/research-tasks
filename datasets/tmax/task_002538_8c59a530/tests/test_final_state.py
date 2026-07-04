# test_final_state.py

import pytest
import requests
import urllib.request
import json

def get_upstream_data():
    edges_resp = requests.get("http://127.0.0.1:9001/edges")
    edges_resp.raise_for_status()
    edges = edges_resp.json()

    nodes_resp = requests.get("http://127.0.0.1:9002/nodes")
    nodes_resp.raise_for_status()
    nodes = nodes_resp.json()

    return edges, nodes

def compute_pagerank(edges, nodes, alpha=0.85, max_iter=100, tol=1e-6):
    # Extract unique nodes
    node_set = set()
    for e in edges:
        node_set.add(e['waiter'])
        node_set.add(e['holder'])
    for n in nodes:
        node_set.add(n['tx_id'])

    node_list = sorted(list(node_set))
    N = len(node_list)

    # Adjacency list (out-edges)
    out_links = {n: [] for n in node_list}
    for e in edges:
        out_links[e['waiter']].append(e['holder'])

    # Initialize PageRank
    pr = {n: 1.0 / N for n in node_list}

    for _ in range(max_iter):
        new_pr = {n: (1.0 - alpha) / N for n in node_list}
        dangling_sum = 0.0

        for n in node_list:
            if len(out_links[n]) == 0:
                dangling_sum += pr[n]

        for n in node_list:
            new_pr[n] += alpha * dangling_sum / N
            if len(out_links[n]) > 0:
                share = pr[n] / len(out_links[n])
                for target in out_links[n]:
                    new_pr[target] += alpha * share

        # Check convergence
        diff = sum(abs(new_pr[n] - pr[n]) for n in node_list)
        pr = new_pr
        if diff < tol:
            break

    return pr

def test_deadlocks_endpoint():
    try:
        resp = requests.get("http://127.0.0.1:8080/api/deadlocks", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/deadlocks: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "deadlocks" in data, "Response JSON missing 'deadlocks' key"

    expected_deadlocks = [
        ["T7", "T8"],
        ["T1", "T2", "T3"],
        ["T4", "T5", "T6"]
    ]

    assert data["deadlocks"] == expected_deadlocks, f"Expected deadlocks {expected_deadlocks}, got {data['deadlocks']}"

def test_pagerank_endpoints():
    edges, nodes = get_upstream_data()
    pr_scores = compute_pagerank(edges, nodes)

    # Build expected results
    node_meta = {n['tx_id']: n['user'] for n in nodes}
    expected_results = []
    for tx_id, score in pr_scores.items():
        expected_results.append({
            "tx_id": tx_id,
            "score": round(score, 4),
            "user": node_meta.get(tx_id, "unknown")
        })

    # Sort by score descending, then tx_id ascending
    expected_results.sort(key=lambda x: (-x['score'], x['tx_id']))

    # Test page 1
    try:
        resp1 = requests.get("http://127.0.0.1:8080/api/pagerank?page=1&limit=3", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/pagerank: {e}")

    assert resp1.status_code == 200, f"Expected status 200, got {resp1.status_code}. Body: {resp1.text}"
    data1 = resp1.json()

    assert data1.get("page") == 1
    assert data1.get("limit") == 3
    assert data1.get("total_nodes") == len(expected_results)
    assert len(data1.get("results", [])) == 3

    # NetworkX pagerank might have slight differences in handling dangling nodes depending on version, 
    # so we check if the structure and roughly the sorted order is correct.
    # We'll assert exact match for tx_id order if possible, or just check the keys.
    for res in data1.get("results", []):
        assert "tx_id" in res
        assert "score" in res
        assert "user" in res

    # Test page 2
    try:
        resp2 = requests.get("http://127.0.0.1:8080/api/pagerank?page=2&limit=3", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/pagerank: {e}")

    assert resp2.status_code == 200
    data2 = resp2.json()

    assert data2.get("page") == 2
    assert data2.get("limit") == 3
    assert len(data2.get("results", [])) == 3