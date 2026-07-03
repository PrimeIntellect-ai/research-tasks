# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fast_kde_exists():
    agent_script = "/home/user/fast_kde.py"
    assert os.path.exists(agent_script), f"Agent script is missing at {agent_script}"
    assert os.path.isfile(agent_script), f"{agent_script} is not a file"

def test_fuzz_equivalence():
    agent_script = "/home/user/fast_kde.py"
    oracle_script = "/app/oracle.py"

    assert os.path.exists(agent_script), "Agent script not found."
    assert os.path.exists(oracle_script), "Oracle script not found."

    random.seed(42)
    charset = "ACGT"
    N = 200

    for i in range(N):
        length = random.randint(10, 500)
        seq = "".join(random.choices(charset, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script],
            input=seq,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input length {length}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=seq,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed or crashed on input length {length}.\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on random input {i+1}/{N} (length {length}).\n"
            f"Input sequence: {seq}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )