# test_final_state.py

import os
import random
import subprocess
import pytest

def test_graph_extraction():
    """Verify that the graph.txt file was correctly extracted from the audio."""
    graph_path = "/home/user/graph.txt"
    assert os.path.isfile(graph_path), f"Graph edge list not found at {graph_path}"

    with open(graph_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_edges = {
        "Alpha,Beta",
        "Beta,Gamma",
        "Alpha,Delta",
        "Gamma,Epsilon",
        "Delta,Zeta"
    }

    actual_edges = set(lines)
    assert actual_edges == expected_edges, f"Graph edges do not match expected. Got: {actual_edges}"

def test_graph_query_fuzz_equivalence():
    """Verify the agent's graph query engine matches the oracle program on random inputs."""
    agent_exec = "/home/user/graph_query"
    oracle_exec = "/app/oracle_graph_query"
    graph_path = "/home/user/graph.txt"

    assert os.path.isfile(agent_exec), f"Agent executable not found at {agent_exec}"
    assert os.access(agent_exec, os.X_OK), f"Agent executable {agent_exec} is not executable"
    assert os.path.isfile(oracle_exec), f"Oracle executable not found at {oracle_exec}"
    assert os.access(oracle_exec, os.X_OK), f"Oracle executable {oracle_exec} is not executable"

    # Generate fuzz input
    random.seed(42)
    nodes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Omega"]
    fuzz_inputs = [random.choice(nodes) for _ in range(100)]
    input_str = "\n".join(fuzz_inputs) + "\n"

    # Run agent
    agent_proc = subprocess.run(
        [agent_exec, graph_path],
        input=input_str,
        text=True,
        capture_output=True,
        timeout=5
    )
    assert agent_proc.returncode == 0, f"Agent program failed with stderr: {agent_proc.stderr}"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_exec, graph_path],
        input=input_str,
        text=True,
        capture_output=True,
        timeout=5
    )
    assert oracle_proc.returncode == 0, f"Oracle program failed with stderr: {oracle_proc.stderr}"

    agent_lines = agent_proc.stdout.strip().split("\n")
    oracle_lines = oracle_proc.stdout.strip().split("\n")

    assert len(agent_lines) == len(oracle_lines), "Agent output line count does not match oracle"

    for i, (agent_line, oracle_line) in enumerate(zip(agent_lines, oracle_lines)):
        assert agent_line == oracle_line, (
            f"Mismatch on input '{fuzz_inputs[i]}'. "
            f"Expected (Oracle): '{oracle_line}', Got (Agent): '{agent_line}'"
        )