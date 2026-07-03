# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/run_resolver_v3.py"
ORACLE_BIN = "/app/oracle_resolver_bin"
N_RUNS = 200

def generate_graph(num_nodes, edge_prob):
    nodes = []
    while len(nodes) < num_nodes:
        name = "".join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))
        if name not in nodes:
            nodes.append(name)
    nodes.sort()

    graph = {node: [] for node in nodes}
    for u in nodes:
        for v in nodes:
            if u != v and random.random() < edge_prob:
                graph[u].append(v)
    return graph

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary at {ORACLE_BIN} is not executable"

    random.seed(42)

    for i in range(N_RUNS):
        num_nodes = random.randint(5, 50)
        graph = generate_graph(num_nodes, 0.3)
        input_json = json.dumps(graph)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_BIN],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_json}\nStderr: {oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed (exit code {agent_proc.returncode}) on input:\n{input_json}\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on run {i+1}/{N_RUNS}.\n"
            f"Input:\n{input_json}\n"
            f"Expected (Oracle):\n{oracle_output}\n"
            f"Got (Agent):\n{agent_output}"
        )