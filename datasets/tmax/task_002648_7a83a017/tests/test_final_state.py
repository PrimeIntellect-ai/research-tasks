# test_final_state.py
import os
import random
import subprocess
import pytest

def test_analyze_seq_fuzz_equivalence():
    """Verify that the agent's compiled C program behaves bit-exactly identically to the oracle."""
    oracle_path = "/app/oracle_analyze"
    agent_path = "/home/user/analyze_seq"

    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable is not executable at {agent_path}"
    assert os.path.isfile(oracle_path), f"Oracle executable not found at {oracle_path}"

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']
    num_iterations = 1000

    for i in range(num_iterations):
        length = random.randint(50, 1000)
        seq = "".join(random.choices(bases, k=length))

        oracle_proc = subprocess.run([oracle_path, seq], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, seq], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input {seq[:50]}..."
        assert agent_proc.returncode == 0, f"Agent failed on input {seq[:50]}...\nError: {agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}, input length {length}.\n"
            f"Input prefix: {seq[:50]}...\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )