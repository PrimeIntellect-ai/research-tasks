# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_fuzz_input():
    num_nodes = random.randint(50, 500)
    num_edges = random.randint(100, 2000)
    num_relations = random.randint(5, 10)

    nodes = [f"N{i}" for i in range(num_nodes)]
    relations = [f"rel{i}" for i in range(num_relations)]

    lines = ["GRAPH"]
    for _ in range(num_edges):
        u = random.choice(nodes)
        v = random.choice(nodes)
        rel = random.choice(relations)
        lines.append(f"{u} {rel} {v}")
    lines.append("END")

    num_queries = 10
    for _ in range(num_queries):
        chain_len = random.randint(1, 4)
        chain = [random.choice(relations) for _ in range(chain_len)]
        lines.append("CHAIN " + " ".join(chain))

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/query_oracle"
    agent_path = "/home/user/graph_query.py"

    assert os.path.exists(agent_path), f"Agent script {agent_path} not found."
    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} not found."

    random.seed(42)

    for i in range(100):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [oracle_path],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr}"

        agent_proc = subprocess.run(
            ["python3", agent_path],
            input=fuzz_input,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed with non-zero exit code on iteration {i}.\nStderr: {agent_proc.stderr}")

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on iteration {i}.\n\n"
                f"--- Input ---\n{fuzz_input}\n"
                f"--- Expected (Oracle) Output ---\n{oracle_proc.stdout}\n"
                f"--- Actual (Agent) Output ---\n{agent_proc.stdout}\n"
            )