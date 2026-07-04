# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_bin = "/home/user/data_processor/processor"
    oracle_bin = "/app/oracle_bin"
    repo_dir = "/home/user/data_processor"

    # Ensure oracle exists
    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    # If agent binary is missing, attempt to build it using make
    if not os.path.isfile(agent_bin):
        try:
            subprocess.run(["make"], cwd=repo_dir, capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary {agent_bin} not found, and 'make' failed to build it.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist even after running make."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

    random.seed(42)
    N = 500

    for _ in range(N):
        a = random.randint(-50, 100)
        b = random.randint(-50, 100)
        c = random.randint(-50, 100)
        args = [str(a), str(b), str(c)]

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin] + args,
            capture_output=True,
            text=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin] + args,
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input {args}.\n"
            f"Expected (Oracle): {oracle_proc.returncode}\n"
            f"Got (Agent): {agent_proc.returncode}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input {args}.\n"
            f"Expected (Oracle): {oracle_proc.stdout!r}\n"
            f"Got (Agent): {agent_proc.stdout!r}"
        )