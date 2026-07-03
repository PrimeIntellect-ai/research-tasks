# test_final_state.py

import os
import subprocess
import pytest
import numpy as np

def generate_test_case():
    """Generate a random near-singular PSD matrix input string."""
    N = np.random.randint(3, 11)
    A = np.random.randn(N, N)
    PSD = (A @ A.T) * 1e-8

    input_lines = [str(N)]
    for row in PSD:
        input_lines.append(" ".join(f"{val:.15e}" for val in row))

    return "\n".join(input_lines) + "\n"

def test_runner_executable_exists():
    """Verify that the agent built the runner executable."""
    assert os.path.isfile('/home/user/runner'), "The executable /home/user/runner is missing."
    assert os.access('/home/user/runner', os.X_OK), "The file /home/user/runner is not executable."

def test_fuzz_equivalence():
    """Fuzz the agent's runner against the oracle with 500 near-singular matrices."""
    np.random.seed(42)
    oracle_path = '/app/oracle'
    agent_path = '/home/user/runner'

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"

    for i in range(500):
        input_data = generate_test_case()

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i}. Input:\n{input_data}\nError: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on iteration {i}. Input:\n{input_data}\nError: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on iteration {i}. Input:\n{input_data}")

        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i}.\n"
            f"Input:\n{input_data}\n"
            f"Expected (Oracle):\n{oracle_output}\n"
            f"Got (Agent):\n{agent_output}"
        )