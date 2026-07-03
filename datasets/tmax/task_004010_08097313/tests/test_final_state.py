# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/primer_model.py"
    oracle_script = "/app/oracle_model.py"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    for i in range(100):
        length = random.randint(50, 500)
        seq = "".join(random.choices(bases, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", oracle_script],
            input=seq,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {seq}\nError: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=seq,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input: {seq}\nError: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i+1}.\n"
            f"Input sequence length: {length}\n"
            f"Input sequence: {seq}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )