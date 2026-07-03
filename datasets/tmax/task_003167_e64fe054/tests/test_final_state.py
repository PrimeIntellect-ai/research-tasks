# test_final_state.py

import os
import subprocess
import random
import pytest

def test_prime_binary_built():
    binary_path = "/app/libprime-1.0.0/prime"
    assert os.path.isfile(binary_path), f"The binary {binary_path} was not built."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

def test_fuzz_equivalence():
    agent_script = "/app/prime_encoder.sh"
    oracle_script = "/opt/oracle/prime_encoder.sh"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."

    random.seed(42)
    inputs = [random.randint(1, 10000) for _ in range(100)]

    for n in inputs:
        str_n = str(n)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script, str_n],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {n}:\n{oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_script, str_n],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {n}:\n{agent_proc.stderr}"
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Mismatch on input {n}.\n"
            f"Expected (Oracle): {repr(oracle_out)}\n"
            f"Actual (Agent): {repr(agent_out)}"
        )