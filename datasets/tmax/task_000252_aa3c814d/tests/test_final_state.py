# test_final_state.py
import os
import subprocess
import time
import random
import pytest

def test_fast_router_exists_and_executable():
    fast_router_path = "/home/user/fast_router"
    assert os.path.exists(fast_router_path), f"Fast router binary is missing at {fast_router_path}"
    assert os.path.isfile(fast_router_path), f"{fast_router_path} is not a file"
    assert os.access(fast_router_path, os.X_OK), f"Fast router binary at {fast_router_path} is not executable"

def test_speedup_and_correctness():
    fast_router_path = "/home/user/fast_router"
    legacy_router_path = "/app/legacy_router"

    test_file = "/tmp/hidden_large_topology.txt"
    num_nodes = 2000
    num_edges = 10000
    start_node = "Node0"
    end_node = f"Node{num_nodes-1}"

    # Generate topology
    random.seed(42)
    with open(test_file, 'w') as f:
        # Create a guaranteed path from Node0 to Node{num_nodes-1}
        for i in range(num_nodes - 1):
            latency = random.randint(1, 10)
            jitter = random.randint(0, 5)
            drop = random.randint(0, 2)
            f.write(f"L_{i} Node{i} Node{i+1} {latency} {jitter} {drop}\n")

        # Add random edges
        for i in range(num_nodes - 1, num_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u == v:
                v = (v + 1) % num_nodes
            latency = random.randint(10, 50)
            jitter = random.randint(5, 15)
            drop = random.randint(1, 5)
            f.write(f"L_{i} Node{u} Node{v} {latency} {jitter} {drop}\n")

    # Run legacy
    t0 = time.time()
    try:
        legacy_out = subprocess.check_output([legacy_router_path, test_file, start_node, end_node], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Legacy router failed: {e}")
    t1 = time.time()
    legacy_time = t1 - t0

    # Run fast
    t2 = time.time()
    try:
        fast_out = subprocess.check_output([fast_router_path, test_file, start_node, end_node], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Fast router failed: {e}")
    t3 = time.time()
    fast_time = t3 - t2

    # Check correctness
    assert legacy_out.strip() == fast_out.strip(), "The output of fast_router does not match legacy_router exactly."

    # Check speedup
    speedup = legacy_time / max(fast_time, 0.001)
    assert speedup >= 50.0, f"Speedup is {speedup:.2f}x, which is less than the required 50.0x threshold."