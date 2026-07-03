# test_final_state.py

import os
import subprocess
import time
import random
import pytest

def test_fast_resolver_performance_and_correctness():
    fast_bin = "/home/user/fast_resolver"
    legacy_bin = "/app/legacy_resolver"

    assert os.path.exists(fast_bin), f"Missing binary: {fast_bin}"
    assert os.access(fast_bin, os.X_OK), f"Binary is not executable: {fast_bin}"

    # Generate a large DAG
    num_nodes = 5000
    num_edges = 20000

    random.seed(42)
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, num_nodes - 2)
        v = random.randint(u + 1, num_nodes - 1)
        edges.add((u, v))

    graph_input = "".join(f"S_{u:04d} S_{v:04d}\n" for u, v in edges)
    graph_bytes = graph_input.encode('utf-8')

    # Run legacy resolver
    t0 = time.time()
    p_legacy = subprocess.run([legacy_bin], input=graph_bytes, capture_output=True)
    t_legacy = time.time() - t0
    assert p_legacy.returncode == 0, f"Legacy resolver failed with error: {p_legacy.stderr.decode()}"

    # Run fast resolver
    t0 = time.time()
    p_fast = subprocess.run([fast_bin], input=graph_bytes, capture_output=True)
    t_fast = time.time() - t0
    assert p_fast.returncode == 0, f"Fast resolver failed with error: {p_fast.stderr.decode()}"

    # Verify correctness
    assert p_fast.stdout == p_legacy.stdout, "Output mismatch between fast_resolver and legacy_resolver on DAG"

    # Verify performance
    speedup = t_legacy / t_fast if t_fast > 0 else float('inf')
    assert speedup >= 4.0, f"Speedup is {speedup:.2f}x (Legacy: {t_legacy:.4f}s, Fast: {t_fast:.4f}s), which is less than the required 4.0x"

def test_fast_resolver_cycle_handling():
    fast_bin = "/home/user/fast_resolver"
    legacy_bin = "/app/legacy_resolver"

    if not os.path.exists(fast_bin):
        pytest.skip("Fast resolver missing")

    # Generate a graph with a cycle
    graph_input = "A B\nB C\nC D\nD B\n".encode('utf-8')

    p_legacy = subprocess.run([legacy_bin], input=graph_input, capture_output=True)
    p_fast = subprocess.run([fast_bin], input=graph_input, capture_output=True)

    assert p_fast.stdout == p_legacy.stdout, "Output mismatch between fast_resolver and legacy_resolver on cyclic graph"