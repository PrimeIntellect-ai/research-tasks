# test_final_state.py
import os
import random
import subprocess
import pytest

def test_plot_exists():
    """Verify that the requested plot was generated."""
    plot_path = "/home/user/plot.png"
    assert os.path.isfile(plot_path), f"The plot file {plot_path} was not generated."

def test_fuzz_equivalence():
    """Fuzz the agent script against the oracle script to verify bit-exact equivalence."""
    oracle_path = "/app/oracle.py"
    agent_path = "/home/user/simulate.py"

    assert os.path.isfile(agent_path), f"Agent script not found at {agent_path}"
    assert os.path.isfile(oracle_path), f"Oracle script not found at {oracle_path}"

    random.seed(42)
    charset = "ACDEFGHIKLMNPQRSTVWY"

    for _ in range(200):
        length = random.randint(10, 100)
        seq = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_cmd = [oracle_path, seq]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {seq}. Stderr: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", agent_path, seq]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {seq}. Stderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input {seq}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )