# test_final_state.py

import json
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/dataset_lineage_oracle"
AGENT_PATH = "/home/user/lineage_solver/target/release/lineage_solver"
FUZZ_N = 200

def generate_random_graph():
    num_nodes = random.randint(10, 100)

    def random_id():
        length = random.randint(2, 5)
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    nodes = [random_id() for _ in range(num_nodes)]
    # Ensure unique nodes
    nodes = list(set(nodes))
    while len(nodes) < num_nodes:
        nodes.append(random_id())
        nodes = list(set(nodes))

    graph = {}
    for node in nodes:
        num_deps = random.randint(0, min(10, len(nodes) - 1))
        deps = {}
        target_nodes = random.sample([n for n in nodes if n != node], num_deps)
        for target in target_nodes:
            deps[target] = random.randint(1, 100)
        graph[node] = {"deps": deps}

    source_node = random.choice(nodes)
    target_node = random.choice(nodes)

    return graph, source_node, target_node

def test_fuzz_equivalence():
    """Fuzz the agent's binary against the oracle to ensure exact output equivalence."""
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary is not executable at {AGENT_PATH}"
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    random.seed(42)

    for i in range(FUZZ_N):
        graph, source, target = generate_random_graph()
        input_json = json.dumps(graph)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, source, target],
                input=input_json,
                text=True,
                capture_output=True,
                timeout=5,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {source} -> {target}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {source} -> {target}.")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH, source, target],
                input=input_json,
                text=True,
                capture_output=True,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input {source} -> {target}.")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent failed with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr}")

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on iteration {i}!\n"
                f"Source: {source}, Target: {target}\n"
                f"Input JSON: {input_json}\n"
                f"Oracle output: {repr(oracle_out)}\n"
                f"Agent output: {repr(agent_out)}"
            )