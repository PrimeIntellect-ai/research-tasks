# test_final_state.py
import os
import subprocess
import random
import pytest

def test_query_tool_equivalence():
    agent_bin = "/home/user/query_tool"
    oracle_bin = "/app/oracle_query_tool"

    assert os.path.isfile(agent_bin), f"Agent executable {agent_bin} not found. Did you compile it?"
    assert os.access(agent_bin, os.X_OK), f"Agent executable {agent_bin} is not executable."
    assert os.path.isfile(oracle_bin), f"Oracle executable {oracle_bin} not found."
    assert os.access(oracle_bin, os.X_OK), f"Oracle executable {oracle_bin} is not executable."

    # Fuzz testing parameters
    random.seed(42)
    num_tests = 50
    test_inputs = [str(random.randint(1, 1000)) for _ in range(num_tests)]

    for val in test_inputs:
        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_bin, val],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            oracle_output = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {val} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {val}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_bin, val],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Your program timed out on input {val}")

        assert agent_res.returncode == 0, f"Your program failed (exit code {agent_res.returncode}) on input {val}. Stderr: {agent_res.stderr}"

        # Compare outputs
        agent_output = agent_res.stdout

        if agent_output != oracle_output:
            pytest.fail(
                f"Output mismatch on input '{val}'.\n"
                f"Expected (Oracle):\n{oracle_output}\n"
                f"Got (Yours):\n{agent_output}"
            )