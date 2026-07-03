# test_final_state.py

import os
import subprocess
import time
import json
import random
import pytest

def test_query_engine_performance():
    init_graph_path = "/home/user/init_graph.csv"
    assert os.path.isfile(init_graph_path), f"Missing {init_graph_path}. You must extract the initial graph from the image."

    engine_path = "/home/user/query_engine"
    assert os.path.isfile(engine_path), f"Missing {engine_path}. You must compile your C program to this path."
    assert os.access(engine_path, os.X_OK), f"{engine_path} is not executable."

    # Generate large dataset
    random.seed(42)
    large_updates_path = '/tmp/large_updates.csv'
    with open(large_updates_path, 'w') as f:
        for _ in range(50000):
            action = random.choice(["ADD", "UPD", "DEL"])
            src = random.randint(1, 1000)
            dst = random.randint(1, 1000)
            cost = round(random.uniform(1.0, 100.0), 1)
            f.write(f"{action},{src},{dst},{cost}\n")

    large_queries_path = '/tmp/large_queries.csv'
    with open(large_queries_path, 'w') as f:
        for _ in range(5000):
            src = random.randint(1, 1000)
            dst = random.randint(1, 1000)
            f.write(f"{src},{dst}\n")

    out_json_path = '/tmp/out.json'
    if os.path.exists(out_json_path):
        os.remove(out_json_path)

    start = time.time()
    result = subprocess.run(
        [engine_path, init_graph_path, large_updates_path, large_queries_path, out_json_path],
        capture_output=True,
        text=True
    )
    end = time.time()

    duration = end - start

    assert result.returncode == 0, f"query_engine failed with return code {result.returncode}.\nstderr: {result.stderr}"
    assert os.path.isfile(out_json_path), f"Output JSON file {out_json_path} was not created."

    try:
        with open(out_json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse output JSON: {e}")

    assert isinstance(data, list), "Output JSON should be a list of objects."
    assert len(data) == 5000, f"Expected 5000 results in output JSON, but got {len(data)}."

    threshold = 0.5
    assert duration <= threshold, f"Execution time {duration:.4f}s exceeded threshold {threshold}s. Your implementation must be further optimized."

def test_init_graph_extraction():
    init_graph_path = "/home/user/init_graph.csv"
    assert os.path.isfile(init_graph_path), f"Missing {init_graph_path}."

    with open(init_graph_path, 'r') as f:
        content = f.read().strip()

    # Check that it extracted the edges properly
    assert "1,2,5.0" in content, "Missing edge 1->2 with cost 5.0 in the extracted CSV."
    assert "1,3,2.0" in content, "Missing edge 1->3 with cost 2.0 in the extracted CSV."
    assert "4,5,3.0" in content, "Missing edge 4->5 with cost 3.0 in the extracted CSV."