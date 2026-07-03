# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def run_engine(pipeline_path, out_path):
    start = time.time()
    cmd = [
        "/app/graph_engine",
        "--nodes", "/home/user/data/nodes.csv",
        "--edges", "/home/user/data/edges.csv",
        "--pipeline", pipeline_path,
        "--out", out_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    duration = time.time() - start

    with open(out_path, "r") as f:
        data = json.load(f)
    return duration, data

def test_optimized_pipeline_exists():
    assert os.path.isfile("/home/user/optimized_pipeline.json"), "/home/user/optimized_pipeline.json is missing"

def test_pipeline_accuracy_and_speedup():
    naive_pipeline = "/home/user/naive_pipeline.json"
    opt_pipeline = "/home/user/optimized_pipeline.json"

    assert os.path.isfile(naive_pipeline), f"{naive_pipeline} is missing"
    assert os.path.isfile(opt_pipeline), f"{opt_pipeline} is missing"

    naive_out_path = "/tmp/naive_out.json"
    opt_out_path = "/tmp/opt_out.json"

    try:
        time_naive, out_naive = run_engine(naive_pipeline, naive_out_path)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run naive pipeline: {e}")

    try:
        time_opt, out_opt = run_engine(opt_pipeline, opt_out_path)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run optimized pipeline: {e}")

    out_naive_sorted = sorted(out_naive, key=lambda x: str(x))
    out_opt_sorted = sorted(out_opt, key=lambda x: str(x))

    assert out_naive_sorted == out_opt_sorted, "The output of the optimized pipeline does not match the naive pipeline."

    speedup = time_naive / time_opt if time_opt > 0 else float('inf')

    assert speedup >= 5.0, f"Speedup is {speedup:.2f}x, which is less than the required 5.0x."