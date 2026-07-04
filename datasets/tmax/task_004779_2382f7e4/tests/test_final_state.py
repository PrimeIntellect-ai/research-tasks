# test_final_state.py
import os
import random
import subprocess
import pytest

def test_agent_executable_exists():
    agent_path = "/home/user/graph_query"
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_graph_query"
    agent_path = "/home/user/graph_query"

    assert os.path.isfile(oracle_path), f"Oracle executable {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} is missing."

    random.seed(12345)

    # Generate 1000 queries
    queries = []
    for _ in range(1000):
        u = random.randint(0, 60)
        v = random.randint(0, 60)
        queries.append(f"{u} {v}")

    input_data = "\n".join(queries) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_path],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    # Run agent
    agent_proc = subprocess.run(
        [agent_path],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )

    assert agent_proc.returncode == 0, f"Agent program crashed or failed: {agent_proc.stderr}"

    oracle_out = oracle_proc.stdout.strip().splitlines()
    agent_out = agent_proc.stdout.strip().splitlines()

    assert len(oracle_out) == len(agent_out), "Agent output line count differs from oracle."

    for i, (q, o_out, a_out) in enumerate(zip(queries, oracle_out, agent_out)):
        assert o_out == a_out, f"Mismatch on query '{q}': expected '{o_out}', got '{a_out}'"