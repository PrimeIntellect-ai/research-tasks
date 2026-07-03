# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_graph_resolver"
AGENT_PATH = "/home/user/workspace/migration-service/target/release/agent_resolver"
NUM_ITERATIONS = 10000

def generate_random_dag():
    n_nodes = random.randint(1, 200)

    # Generate unique random alphanumeric node names
    nodes = set()
    while len(nodes) < n_nodes:
        length = random.randint(4, 12)
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        nodes.add(name)
    nodes = list(nodes)

    # Create a random topological order to guarantee a DAG
    topological_order = nodes[:]
    random.shuffle(topological_order)

    # Generate all possible valid edges
    possible_edges = []
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            possible_edges.append((topological_order[i], topological_order[j]))

    max_edges = len(possible_edges)
    e_edges = random.randint(0, max_edges)

    # Sample E edges
    edges = random.sample(possible_edges, e_edges)

    # Construct the input string
    lines = []
    lines.append(str(n_nodes))
    for node in nodes:
        lines.append(node)
    lines.append(str(e_edges))
    for src, dst in edges:
        lines.append(f"{src} {dst}")

    return "\n".join(lines) + "\n"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)

    # Run a subset for speed if 10000 is too slow in python, but the spec says 10000.
    # To optimize, we can use subprocess.Popen and communicate, or just run them.
    # Let's run 10000 iterations as requested.
    for i in range(NUM_ITERATIONS):
        dag_input = generate_random_dag()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=dag_input,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with input:\n{dag_input}\nStderr: {oracle_proc.stderr}"

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=dag_input,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent failed on iteration {i} with input:\n{dag_input}\nStderr: {agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}!\n"
                f"Input:\n{dag_input}\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}\n"
            )