# test_final_state.py

import os
import subprocess
import random
import pytest

def test_solution_exists():
    assert os.path.exists("/home/user/solution.py"), "Solution file /home/user/solution.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_calc"
    agent_path = "/home/user/solution.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent solution missing at {agent_path}"

    random.seed(42)
    # Fuzz-input distribution: N=1000, uniform [0.0, 1e15]
    inputs = [random.uniform(0.0, 1e15) for _ in range(1000)]

    # Include some boundary and specific edge cases
    inputs.extend([0.0, 1.0, 1e12, 1e15])

    for val in inputs:
        # Format to avoid overly long string representations, standard float string
        str_val = str(val)

        oracle_cmd = [oracle_path, str_val]
        agent_cmd = ["python3", agent_path, str_val]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True, timeout=2)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {str_val}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {str_val}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True, timeout=2)
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent solution failed on input {str_val}:\nStdout: {e.stdout}\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent solution timed out on input {str_val}")

        assert oracle_out == agent_out, f"Mismatch on input {str_val}:\nOracle: '{oracle_out}'\nAgent : '{agent_out}'"