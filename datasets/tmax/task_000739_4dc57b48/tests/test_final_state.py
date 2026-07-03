# test_final_state.py

import os
import json
import math

def compute_pagerank(edges, alpha=0.85, max_iter=100, tol=1e-6):
    """
    Computes PageRank using standard library, mirroring networkx.pagerank behavior.
    edges is a list of tuples: (u, v, weight)
    """
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)

    N = len(nodes)
    if N == 0:
        return {}

    out_weight = {n: 0.0 for n in nodes}
    for u, v, w in edges:
        out_weight[u] += w

    pr = {n: 1.0 / N for n in nodes}

    for _ in range(max_iter):
        prev_pr = pr.copy()

        dangling_sum = sum(prev_pr[n] for n in nodes if out_weight[n] == 0)

        for n in nodes:
            pr[n] = (1.0 - alpha) / N + alpha * dangling_sum / N

        for u, v, w in edges:
            pr[v] += alpha * prev_pr[u] * w / out_weight[u]

        err = sum(abs(pr[n] - prev_pr[n]) for n in nodes)
        if err < N * tol:
            break

    return pr

def test_pagerank_results():
    input_file = "/home/user/raw_citations.jsonl"
    output_file = "/home/user/pagerank.json"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Did the script run and save the output?"

    # 1. Read and clean data exactly as specified
    papers = {}
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            pid = record["paper_id"]

            if pid not in papers or record["timestamp"] > papers[pid]["timestamp"]:
                papers[pid] = record

    # Filter deleted
    valid_papers = [p for p in papers.values() if not p.get("is_deleted", False)]

    # 2. Aggregate edges
    edge_weights = {}
    for p in valid_papers:
        u = p["author"]
        v = p["cited_author"]
        edge_weights[(u, v)] = edge_weights.get((u, v), 0) + 1

    edges = [(u, v, w) for (u, v), w in edge_weights.items()]

    # 3. Compute expected PageRank
    expected_pr = compute_pagerank(edges)

    # 4. Read actual PageRank
    with open(output_file, "r") as f:
        try:
            actual_pr = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Output file {output_file} is not valid JSON."

    # 5. Compare
    assert isinstance(actual_pr, dict), f"Expected JSON object (dict) in {output_file}, got {type(actual_pr)}"

    missing_nodes = set(expected_pr.keys()) - set(actual_pr.keys())
    extra_nodes = set(actual_pr.keys()) - set(expected_pr.keys())

    assert not missing_nodes, f"Missing authors in PageRank output: {missing_nodes}"
    assert not extra_nodes, f"Unexpected authors in PageRank output: {extra_nodes}"

    for node, expected_score in expected_pr.items():
        actual_score = actual_pr[node]
        assert isinstance(actual_score, (int, float)), f"Score for {node} is not a number: {actual_score}"
        assert math.isclose(actual_score, expected_score, abs_tol=1e-4), \
            f"Mismatch for {node}: expected {expected_score:.5f}, got {actual_score:.5f}"