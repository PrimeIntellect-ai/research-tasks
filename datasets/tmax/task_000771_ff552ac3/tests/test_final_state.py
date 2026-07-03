# test_final_state.py
import os
import sys
import json
import random
import subprocess
import tempfile
import pytest

def generate_random_tree(num_nodes):
    nodes = []
    edges = []

    # Create nodes
    for i in range(1, num_nodes + 1):
        nodes.append({"id": i, "value": random.randint(1, 1000)})

    # Create edges to form a tree
    # Node 1 is root. For node i (2 to num_nodes), pick a parent from 1 to i-1.
    for i in range(2, num_nodes + 1):
        parent = random.randint(1, i - 1)
        edges.append({"parent": parent, "child": i})

    # Shuffle nodes and edges so they aren't trivially sorted
    random.shuffle(nodes)
    random.shuffle(edges)

    return {"nodes": nodes, "edges": edges}

def test_executor_fixed():
    executor_path = "/app/sql-graph-emulator/sge/executor.py"
    assert os.path.isfile(executor_path), f"File {executor_path} is missing."

    with open(executor_path, "r") as f:
        content = f.read()

    # Check that the implicit cross join was fixed (an 'if' condition checking parent/child was added)
    assert "if" in content and "child" in content and "parent" in content, (
        "The _join_edges method in executor.py does not appear to be fixed. "
        "It still lacks a proper join condition."
    )

def test_fuzz_equivalence():
    agent_script = "/home/user/solve.py"
    oracle_script = "/opt/oracle/solve_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(50):
            num_nodes = random.randint(10, 100)
            data = generate_random_tree(num_nodes)

            input_path = os.path.join(tmpdir, f"input_{i}.json")
            with open(input_path, "w") as f:
                json.dump(data, f)

            # Run oracle
            oracle_proc = subprocess.run(
                [sys.executable, oracle_script, input_path],
                capture_output=True, text=True, check=True
            )
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(
                [sys.executable, agent_script, input_path],
                capture_output=True, text=True
            )

            assert agent_proc.returncode == 0, (
                f"Agent script failed on iteration {i}.\n"
                f"Input: {json.dumps(data)}\n"
                f"Stderr:\n{agent_proc.stderr}"
            )

            agent_out = agent_proc.stdout

            if agent_out != oracle_out:
                pytest.fail(
                    f"Mismatch on iteration {i}.\n"
                    f"Input: {json.dumps(data)}\n"
                    f"Oracle output:\n{oracle_out}\n"
                    f"Agent output:\n{agent_out}"
                )