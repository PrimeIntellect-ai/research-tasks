# test_final_state.py
import os
import time
import subprocess
import pytest
import pandas as pd
import numpy as np

def generate_graph(num_nodes, num_edges, output_path):
    np.random.seed(42)
    sources = np.random.randint(1, num_nodes + 1, num_edges)
    targets = np.random.randint(1, num_nodes + 1, num_edges)
    df = pd.DataFrame({'source': sources, 'target': targets})
    df.to_csv(output_path, index=False)
    return len(np.unique(np.concatenate([sources, targets])))

def test_fast_graph_exists():
    binary_path = "/home/user/fast_graph"
    assert os.path.exists(binary_path), f"Expected binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"Expected {binary_path} to be a file."
    assert os.access(binary_path, os.X_OK), f"Expected {binary_path} to be executable."

def test_correctness_against_oracle():
    input_csv = "/tmp/small_graph.csv"
    oracle_out = "/tmp/oracle_small_out.csv"
    fast_out = "/tmp/fast_small_out.csv"

    generate_graph(10_000, 50_000, input_csv)

    # Run oracle
    subprocess.run(["/app/graph_oracle", input_csv, oracle_out], check=True)

    # Run fast_graph
    subprocess.run(["/home/user/fast_graph", input_csv, fast_out], check=True)

    df_expected = pd.read_csv(oracle_out)
    df_actual = pd.read_csv(fast_out)

    pd.testing.assert_frame_equal(df_expected, df_actual, check_dtype=False, obj="Correctness on small graph")

def test_performance():
    input_csv = "/tmp/large_graph.csv"
    fast_out = "/tmp/fast_large_out.csv"

    num_unique_nodes = generate_graph(1_000_000, 5_000_000, input_csv)

    start_time = time.time()
    subprocess.run(["/home/user/fast_graph", input_csv, fast_out], check=True)
    duration = time.time() - start_time

    assert duration <= 2.0, f"Performance failed: execution took {duration:.2f} seconds (threshold is 2.0s)."

    # Basic sanity check on large output
    df_actual = pd.read_csv(fast_out)
    assert len(df_actual) == num_unique_nodes, f"Expected {num_unique_nodes} rows in output, got {len(df_actual)}."
    assert list(df_actual.columns) == ["node", "component_id", "degree", "rank"], "Output columns are incorrect."