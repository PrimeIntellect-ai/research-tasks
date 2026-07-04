# test_final_state.py

import os
import json
import time
import sys
import importlib.util
from collections import defaultdict

def get_truth_centrality(data_path):
    centrality = defaultdict(int)
    with open(data_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            paper = json.loads(line)
            year = paper.get("year", 0)
            if year >= 2010:
                authors = paper.get("authors", [])
                num_authors = len(authors)
                if num_authors > 1:
                    for author in authors:
                        centrality[author] += (num_authors - 1)
    return dict(centrality)

def test_results_exist_and_accurate():
    results_path = "/home/user/centrality_results.json"
    data_path = "/home/user/data/papers.jsonl"

    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        student_results = json.load(f)

    truth_results = get_truth_centrality(data_path)

    # Check MSE == 0.0 (exact match)
    all_authors = set(student_results.keys()).union(set(truth_results.keys()))
    mse = 0.0
    for author in all_authors:
        student_val = student_results.get(author, 0)
        truth_val = truth_results.get(author, 0)
        mse += (student_val - truth_val) ** 2

    if len(all_authors) > 0:
        mse /= len(all_authors)

    assert mse == 0.0, f"MSE is {mse}, expected 0.0. Centrality results do not match ground truth."

def test_speedup_metric():
    # Load the agent's module
    executor_path = "/app/vendored/py-graph-engine/core/executor.py"
    assert os.path.isfile(executor_path), "Executor file missing"

    spec = importlib.util.spec_from_file_location("executor", executor_path)
    executor = importlib.util.module_from_spec(spec)
    sys.modules["executor"] = executor
    spec.loader.exec_module(executor)

    # Generate synthetic data for benchmark
    N = 2000
    sources = [{'node_id': f's_{i}', 'ref_id': f't_{i % 500}', 'weight': 1} for i in range(N)]
    targets = [{'node_id': f't_{i}', 'val': i} for i in range(500)]

    # Benchmark agent's implementation
    start = time.perf_counter()
    agent_edges = executor.build_edge_list(sources, targets)
    agent_time = time.perf_counter() - start

    # Unoptimized O(N^2) implementation for baseline
    def unoptimized_build_edge_list(srcs, tgts):
        edges = []
        for s in srcs:
            for t in tgts:
                if s['ref_id'] == t['node_id']:
                    edges.append((s['node_id'], t['node_id'], s['weight']))
        return edges

    start_unopt = time.perf_counter()
    unopt_edges = unoptimized_build_edge_list(sources, targets)
    unopt_time = time.perf_counter() - start_unopt

    assert len(agent_edges) == len(unopt_edges), "Agent's build_edge_list returned incorrect number of edges"

    speedup = unopt_time / max(agent_time, 1e-6)
    assert speedup >= 20.0, f"Speedup is {speedup:.2f}x, expected >= 20.0x"