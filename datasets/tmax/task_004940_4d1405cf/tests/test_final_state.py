# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE_PATH = "/opt/verifier/reference_graph_analyzer"
AGENT_PATH = "/home/user/graph_analyzer"
NUM_FUZZ_TESTS = 50

def generate_csv_data(fuzz_dir, seed):
    rng = random.Random(seed)

    num_nodes = rng.randint(100, 1000)
    nodes = []
    # node_id,category,value
    categories = ['A', 'B', 'C', 'D', 'E', 'X', 'Y'] # ensure X and Y are present as per image

    # Ensure unique node IDs
    node_ids = rng.sample(range(1, 2000), num_nodes)

    with open(os.path.join(fuzz_dir, "nodes.csv"), "w") as f:
        for nid in node_ids:
            cat = rng.choice(categories)
            val = rng.randint(1, 100)
            f.write(f"{nid},{cat},{val}\n")
            nodes.append(nid)

    num_edges = rng.randint(500, 5000)
    with open(os.path.join(fuzz_dir, "edges.csv"), "w") as f:
        for _ in range(num_edges):
            src = rng.choice(nodes)
            tgt = rng.choice(nodes)
            weight = rng.randint(1, 1000)
            f.write(f"{src},{tgt},{weight}\n")

@pytest.mark.parametrize("seed", range(NUM_FUZZ_TESTS))
def test_fuzz_equivalence(seed):
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} not found. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} not found."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    with tempfile.TemporaryDirectory() as fuzz_dir:
        generate_csv_data(fuzz_dir, seed)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH, fuzz_dir],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on seed {seed}:\n{oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH, fuzz_dir],
            capture_output=True,
            text=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent program failed with return code {agent_proc.returncode} on seed {seed}.\nStderr: {agent_proc.stderr}")

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            # truncate output for display if too long
            disp_oracle = oracle_out if len(oracle_out) < 1000 else oracle_out[:1000] + "\n...[truncated]"
            disp_agent = agent_out if len(agent_out) < 1000 else agent_out[:1000] + "\n...[truncated]"
            pytest.fail(
                f"Mismatch on seed {seed}.\n"
                f"--- Oracle Output ---\n{disp_oracle}\n"
                f"--- Agent Output ---\n{disp_agent}\n"
            )