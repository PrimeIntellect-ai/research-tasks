# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_BIN = "/app/dataset_analyzer"
AGENT_BIN = "/home/user/solution"

def generate_random_graph_and_queries(seed):
    random.seed(seed)

    V = random.randint(10, 1000)
    max_edges = min(V * (V - 1), 10000)
    E = random.randint(min(V, max_edges), max_edges)

    edges = set()
    while len(edges) < E:
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u != v:
            edges.add((u, v))

    Q = random.randint(50, 500)
    queries = []

    for _ in range(Q):
        q_type = random.choice(["CENTRALITY", "CO_CITE", "PATTERN"])
        if q_type == "CENTRALITY":
            u = random.randint(0, V - 1)
            queries.append(f"CENTRALITY {u}")
        elif q_type == "CO_CITE":
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            queries.append(f"CO_CITE {u} {v}")
        elif q_type == "PATTERN":
            u = random.randint(0, V - 1)
            queries.append(f"PATTERN {u}")

    input_lines = []
    input_lines.append(f"{V} {E}")
    for u, v in edges:
        input_lines.append(f"{u} {v}")
    input_lines.append(f"{Q}")
    input_lines.extend(queries)

    return "\n".join(input_lines) + "\n"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.path.isfile(AGENT_BIN), f"Path {AGENT_BIN} is not a file"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BIN), f"Oracle binary missing at {ORACLE_BIN}"
    assert os.path.exists(AGENT_BIN), f"Agent binary missing at {AGENT_BIN}"

    N = 100
    for i in range(N):
        input_data = generate_random_graph_and_queries(seed=42 + i)

        oracle_proc = subprocess.run(
            [ORACLE_BIN],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        assert oracle_proc.returncode == 0, f"Oracle binary failed on iteration {i} with error: {oracle_proc.stderr}"

        agent_proc = subprocess.run(
            [AGENT_BIN],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent binary crashed/failed on iteration {i}. Stderr: {agent_proc.stderr}")

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"--- Input (first 10 lines) ---\n"
                f"{chr(10).join(input_data.splitlines()[:10])}\n...\n"
                f"--- Expected Output (Oracle) ---\n{oracle_out}\n"
                f"--- Actual Output (Agent) ---\n{agent_out}"
            )