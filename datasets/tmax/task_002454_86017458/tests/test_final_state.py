# test_final_state.py

import os
import random
import subprocess
import pytest

def test_bio_scorer_exists_and_executable():
    """Test that the agent's compiled binary exists and is executable."""
    agent_binary = "/home/user/bio_scorer"
    assert os.path.isfile(agent_binary), f"Expected agent binary is missing: {agent_binary}"
    assert os.access(agent_binary, os.X_OK), f"Agent binary is not executable: {agent_binary}"

def test_fuzz_equivalence():
    """Test that the agent's binary is bit-exact equivalent to the oracle on random DNA sequences."""
    agent_binary = "/home/user/bio_scorer"
    oracle_binary = "/app/oracle_scorer"

    assert os.path.isfile(agent_binary), f"Agent binary missing: {agent_binary}"
    assert os.path.isfile(oracle_binary), f"Oracle binary missing: {oracle_binary}"

    random.seed(42)
    nucleotides = ['A', 'C', 'G', 'T']
    num_iterations = 1000

    for i in range(num_iterations):
        length = random.randint(1, 1024)
        dna_sequence = "".join(random.choices(nucleotides, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_binary, dna_sequence],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {dna_sequence}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_binary, dna_sequence],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent binary failed (exit code {agent_proc.returncode}) on input: {dna_sequence}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on iteration {i+1}.\n"
            f"Input length: {length}\n"
            f"Input sequence: {dna_sequence}\n"
            f"Oracle output: '{oracle_output}'\n"
            f"Agent output: '{agent_output}'"
        )