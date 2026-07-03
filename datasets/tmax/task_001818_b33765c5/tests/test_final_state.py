# test_final_state.py
import os
import time
import random
import subprocess
import pytest

def test_fast_query_script_exists():
    script_path = "/home/user/fast_query.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(script_path), f"Script is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_fast_query_accuracy_and_performance(tmp_path):
    script_path = "/home/user/fast_query.sh"
    oracle_path = "/app/citation_oracle"

    edgelist_file = tmp_path / "edgelist.txt"
    queries_file = tmp_path / "queries.txt"

    # Generate a random graph with 1000 nodes and 10000 edges
    random.seed(42)
    nodes = 1000
    edges = 10000

    with open(edgelist_file, "w") as f:
        for _ in range(edges):
            u = random.randint(1, nodes)
            v = random.randint(1, nodes)
            f.write(f"{u} {v}\n")

    # Generate 100 queries
    num_queries = 100
    queries = []
    with open(queries_file, "w") as f:
        for _ in range(num_queries):
            u = random.randint(1, nodes)
            v = random.randint(1, nodes)
            queries.append((u, v))
            f.write(f"{u} {v}\n")

    # Run the oracle to get ground truth
    ground_truth = []
    for u, v in queries:
        res = subprocess.run(
            [oracle_path, str(edgelist_file), str(u), str(v)],
            capture_output=True,
            text=True,
            check=True
        )
        ground_truth.append(res.stdout.strip())

    # Run the student's script and measure runtime
    start_time = time.time()
    res = subprocess.run(
        ["bash", script_path, str(edgelist_file), str(queries_file)],
        capture_output=True,
        text=True
    )
    runtime = time.time() - start_time

    # Check execution success
    assert res.returncode == 0, f"Script failed with error:\n{res.stderr}"

    # Check accuracy
    outputs = res.stdout.strip().split('\n')
    assert len(outputs) == len(ground_truth), f"Expected {len(ground_truth)} output lines, got {len(outputs)}"

    for i, (out, truth) in enumerate(zip(outputs, ground_truth)):
        assert out == truth, f"Query {i+1} ({queries[i][0]} -> {queries[i][1]}): expected {truth}, got {out}"

    # Check performance threshold
    threshold = 3.0
    assert runtime <= threshold, f"Runtime {runtime:.2f}s exceeded {threshold}s threshold."