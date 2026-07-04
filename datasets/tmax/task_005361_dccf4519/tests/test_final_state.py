# test_final_state.py

import os
import time
import subprocess
import numpy as np
import pytest

def generate_graph(n, p, filename):
    # Generate random directed graph
    adj = np.random.rand(n, n) < p
    np.fill_diagonal(adj, False)
    sources, targets = np.where(adj)
    edges = np.column_stack((sources, targets))
    np.savetxt(filename, edges, fmt='%d', delimiter='\t')

def test_fast_centrality_speedup():
    agent_script = "/home/user/fast_centrality.sh"
    oracle_binary = "/app/graph_oracle"
    test_graph = "/tmp/test_graph.txt"
    oracle_out = "/tmp/oracle_out.txt"
    agent_out = "/tmp/agent_out.txt"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_binary), f"Oracle binary not found at {oracle_binary}"

    # 1. Generate test graph
    n = 5000
    p = 0.002
    generate_graph(n, p, test_graph)

    # 2. Run oracle
    t0 = time.time()
    subprocess.run([oracle_binary, test_graph, oracle_out], check=True)
    t_oracle = time.time() - t0

    # 3. Run agent script
    t0 = time.time()
    subprocess.run(["bash", agent_script, test_graph, agent_out], check=True)
    t_agent = time.time() - t0

    # 4. Compare outputs
    assert os.path.exists(oracle_out), "Oracle output missing"
    assert os.path.exists(agent_out), "Agent output missing"

    oracle_data = np.loadtxt(oracle_out)
    agent_data = np.loadtxt(agent_out)

    assert oracle_data.shape == agent_data.shape, "Output dimensions mismatch"
    assert np.array_equal(oracle_data[:, 0], agent_data[:, 0]), "Node IDs mismatch between oracle and agent"

    mse = np.mean((oracle_data[:, 1] - agent_data[:, 1])**2)
    assert mse < 0.0001, f"MSE is too high: {mse:.6f} >= 0.0001. Agent output is not functionally equivalent."

    # 5. Check speedup
    speedup = t_oracle / max(t_agent, 1e-6)
    assert speedup >= 10.0, f"Speedup is {speedup:.2f}x, which is below the threshold of 10.0x (Oracle: {t_oracle:.2f}s, Agent: {t_agent:.2f}s)"