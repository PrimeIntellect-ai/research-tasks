# test_final_state.py

import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/app/sql_generator"
AGENT_PATH = "/home/user/generate_sql"

def generate_random_input():
    # Path lengths: 2 to 6 nodes
    path_len = random.randint(2, 6)
    # Generate aliases (A, B, C...)
    aliases = list(string.ascii_uppercase[:path_len])
    path_str = "->".join(f"({a})" for a in aliases)

    # Nodes: 1 to 10 random integers between 1 and 999
    num_nodes = random.randint(1, 10)
    nodes = [str(random.randint(1, 999)) for _ in range(num_nodes)]
    nodes_str = ",".join(nodes)

    return f"GRAPH_UPDATE path={path_str} nodes={nodes_str}"

def test_binaries_exist():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing: {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary not executable: {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent binary missing: {AGENT_PATH}. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(100):
        test_input = generate_random_input()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input: {test_input}\nError: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input: {test_input}\nError: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i+1}!\n"
            f"Input: {test_input}\n"
            f"Expected (Oracle):\n{oracle_output}\n"
            f"Got (Agent):\n{agent_output}"
        )