# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    """
    Validates the agent's query solver against the oracle program using fuzz testing.
    Generates 1000 random queries, runs both programs, and asserts bit-exact output equivalence.
    """
    oracle_path = "/opt/oracle/fuzz_oracle_dijkstra"
    agent_path = "/home/user/query_solver.sh"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    # Generate 1000 random queries (node IDs between 0 and 500)
    random.seed(42)
    inputs = []
    for _ in range(1000):
        u = random.randint(0, 500)
        v = random.randint(0, 500)
        inputs.append(f"{u} {v}")

    input_str = "\n".join(inputs) + "\n"

    # Run Oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_path], 
            input=input_str, 
            text=True, 
            capture_output=True, 
            timeout=15
        )
        oracle_out = oracle_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle program timed out.")

    # Run Agent
    try:
        agent_proc = subprocess.run(
            ["bash", agent_path], 
            input=input_str, 
            text=True, 
            capture_output=True, 
            timeout=15
        )
        agent_out = agent_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out. Ensure the C++ code is optimized for up to 10,000 queries.")

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent script failed with return code {agent_proc.returncode}.\nStderr:\n{agent_proc.stderr}")

    oracle_lines = [line.strip() for line in oracle_out.strip().split('\n') if line.strip()]
    agent_lines = [line.strip() for line in agent_out.strip().split('\n') if line.strip()]

    assert len(oracle_lines) == len(agent_lines), (
        f"Output length mismatch: Oracle produced {len(oracle_lines)} lines, "
        f"Agent produced {len(agent_lines)} lines."
    )

    for i, (o, a) in enumerate(zip(oracle_lines, agent_lines)):
        assert o == a, (
            f"Mismatch on query {i+1} (Input: '{inputs[i]}'):\n"
            f"Expected (Oracle): {o}\n"
            f"Got (Agent):       {a}"
        )