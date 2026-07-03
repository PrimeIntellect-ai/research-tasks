# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_input(seed):
    random.seed(seed)
    length = random.randint(10, 1000)
    seq = ''.join(random.choices("ACGT", k=length))
    seq_lines = '\n'.join([seq[i:i+80] for i in range(0, len(seq), 80)])
    return f">fuzz_seq_{length}\n{seq_lines}\n"

def test_fuzz_equivalence():
    agent_solver = "/home/user/solver"
    oracle_solver = "/app/oracle_solver"

    assert os.path.isfile(agent_solver), f"Agent solver executable {agent_solver} is missing."
    assert os.access(agent_solver, os.X_OK), f"Agent solver {agent_solver} is not executable."
    assert os.path.isfile(oracle_solver), f"Oracle solver {oracle_solver} is missing."
    assert os.access(oracle_solver, os.X_OK), f"Oracle solver {oracle_solver} is not executable."

    num_inputs = 50
    for i in range(num_inputs):
        fuzz_input = generate_input(i)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_solver],
                input=fuzz_input,
                text=True,
                capture_output=True,
                timeout=5,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {i}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_solver],
                input=fuzz_input,
                text=True,
                capture_output=True,
                timeout=5,
                check=True
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {i}")

        assert oracle_out == agent_out, (
            f"Mismatch on input {i}:\n"
            f"Input:\n{fuzz_input}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )