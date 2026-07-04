# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fixed_query_exists():
    path = "/home/user/fixed_query.py"
    assert os.path.isfile(path), f"Agent's script is missing: {path}"

def test_fuzz_equivalence():
    agent_script = "/home/user/fixed_query.py"
    oracle_binary = "/app/oracle_query"

    assert os.path.isfile(agent_script), f"Agent's script is missing: {agent_script}"
    assert os.path.isfile(oracle_binary), f"Oracle binary is missing: {oracle_binary}"
    assert os.access(oracle_binary, os.X_OK), f"Oracle binary is not executable: {oracle_binary}"

    # Generate 1000 random 32-bit unsigned integers
    random.seed(42)
    test_inputs = [random.randint(0, 4294967295) for _ in range(1000)]

    for val in test_inputs:
        val_str = str(val)

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_binary, val_str],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input {val_str}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed on input {val_str} with error: {e.stderr}")

        # Run agent script
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, val_str],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent's script timed out on input {val_str}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent's script failed on input {val_str} with error: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {val_str}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )