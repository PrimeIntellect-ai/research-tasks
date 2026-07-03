# test_final_state.py
import os
import json
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/cluster_verifier"
AGENT_SCRIPT = "/home/user/verify_clusters.py"

def generate_random_graph_csv(filepath, num_nodes, num_edges):
    # Select random node IDs
    node_ids = random.sample(range(1, 100001), num_nodes)

    with open(filepath, 'w') as f:
        for _ in range(num_edges):
            u = random.choice(node_ids)
            v = random.choice(node_ids)
            f.write(f"{u},{v}\n")

@pytest.mark.parametrize("iteration", range(100))
def test_fuzz_equivalence(iteration):
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing: {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"

    # Deterministic randomness for reproducibility
    random.seed(42 + iteration)

    num_nodes = random.randint(50, 5000)
    num_edges = random.randint(0, 20000)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv = os.path.join(tmpdir, "input.csv")
        oracle_out = os.path.join(tmpdir, "oracle.json")
        agent_out = os.path.join(tmpdir, "agent.json")

        generate_random_graph_csv(input_csv, num_nodes, num_edges)

        # Run Oracle
        oracle_cmd = [ORACLE_PATH, "--in", input_csv, "--out", oracle_out]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {iteration}. Stderr: {oracle_proc.stderr}"

        # Run Agent
        agent_cmd = ["python3", AGENT_SCRIPT, "--in", input_csv, "--out", agent_out]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on iteration {iteration}. Stderr: {agent_proc.stderr}"

        # Compare outputs
        assert os.path.exists(oracle_out), "Oracle output JSON missing."
        assert os.path.exists(agent_out), "Agent output JSON missing."

        with open(oracle_out, 'r') as f:
            try:
                oracle_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("Oracle output is not valid JSON.")

        with open(agent_out, 'r') as f:
            try:
                agent_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("Agent output is not valid JSON.")

        if oracle_data != agent_data:
            # Optionally, show some diff if it's small, or just fail
            pytest.fail(f"Mismatch on iteration {iteration} ({num_nodes} nodes, {num_edges} edges).\n"
                        f"Oracle keys: {len(oracle_data)}, Agent keys: {len(agent_data)}")