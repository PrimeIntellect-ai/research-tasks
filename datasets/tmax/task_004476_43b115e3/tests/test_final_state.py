# test_final_state.py

import json
import random
import subprocess
import os
import tempfile
import pytest

def generate_graph(seed):
    random.seed(seed)
    n = random.randint(10, 50)
    p = random.uniform(0.1, 0.3)

    node_ids = random.sample(range(1, 1000), n) # Using 1-1000 to easily get 50 unique IDs
    nodes = [{"id": nid, "size": random.randint(10, 1000)} for nid in node_ids]

    edges = []
    for i in node_ids:
        for j in node_ids:
            if i != j and random.random() < p:
                edges.append({
                    "source": i,
                    "target": j,
                    "transfer_time": random.randint(1, 20)
                })

    return {"nodes": nodes, "edges": edges}

def test_fuzz_equivalence():
    agent_script = "/home/user/backup_planner.py"
    oracle_bin = "/app/backup_path_oracle"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            graph_data = generate_graph(i)
            input_path = os.path.join(tmpdir, f"graph_{i}.json")
            with open(input_path, "w") as f:
                json.dump(graph_data, f)

            # Run oracle
            oracle_res = subprocess.run([oracle_bin, input_path], capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on input {i}:\n{oracle_res.stderr}"
            oracle_out = oracle_res.stdout.strip()

            # Run agent
            agent_res = subprocess.run(["python3", agent_script, input_path], capture_output=True, text=True)
            if agent_res.returncode != 0:
                pytest.fail(f"Agent script failed on input {i}:\n{agent_res.stderr}")
            agent_out = agent_res.stdout.strip()

            if oracle_out != agent_out:
                pytest.fail(
                    f"Mismatch on random input {i} (seed {i}).\n"
                    f"Graph Data: {json.dumps(graph_data)}\n"
                    f"Expected (Oracle): {oracle_out}\n"
                    f"Got (Agent):       {agent_out}"
                )