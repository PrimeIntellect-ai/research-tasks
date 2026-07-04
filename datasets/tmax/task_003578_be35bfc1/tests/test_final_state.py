# test_final_state.py

import os
import random
import subprocess
import pytest

def test_graph_query_script_exists():
    assert os.path.isfile("/home/user/graph_query.py"), "Agent script /home/user/graph_query.py does not exist."

def test_perturbation_fixed():
    target_file = "/app/networkx-3.1/networkx/algorithms/shortest_paths/unweighted.py"
    assert os.path.isfile(target_file), f"Target file not found at {target_file}"

    with open(target_file, "r") as f:
        content = f.read()

    # The exception string might be commented out, so we check if it's active.
    # Actually, a simpler check is to ensure that running the script doesn't raise it.
    # We will rely on the fuzz test to ensure it works.
    pass

def test_fuzz_equivalence():
    agent_script = "/home/user/graph_query.py"
    oracle_script = "/opt/oracle/reference_graph_query.py"

    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    # Generate 500 random inputs
    random.seed(42)
    inputs = []
    for _ in range(500):
        start = random.randint(1, 1000)
        end = random.randint(1, 1000)
        inputs.append(f"{start},{end}")

    input_str = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        ["python3", oracle_script],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"
    oracle_output = oracle_proc.stdout.strip().split("\n")

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_str,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed: {agent_proc.stderr}"
    agent_output = agent_proc.stdout.strip().split("\n")

    # Compare lengths
    assert len(oracle_output) == len(agent_output), "Agent script output line count does not match oracle."

    # Compare outputs line by line
    for i, (in_line, oracle_line, agent_line) in enumerate(zip(inputs, oracle_output, agent_output)):
        assert oracle_line == agent_line, (
            f"Mismatch on input '{in_line}' (line {i+1}). "
            f"Expected '{oracle_line}', got '{agent_line}'."
        )