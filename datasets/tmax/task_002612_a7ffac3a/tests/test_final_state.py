# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_route_degree"
AGENT_PATH = "/home/user/route_degree"
N_TESTS = 40

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}. Did you compile your C program to the correct path?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    random.seed(42)
    inputs = [random.randint(0, 100) for _ in range(N_TESTS)]

    # Explicitly include the known corrupted nodes from the image to ensure they are tested
    # even if the random seed doesn't happen to pick them.
    corrupted_nodes = [14, 27, 55, 91]
    for node in corrupted_nodes:
        if node not in inputs:
            inputs.append(node)

    for val in inputs:
        val_str = str(val)

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_PATH, val_str],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {val_str} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {val_str}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [AGENT_PATH, val_str],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {val_str} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {val_str}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input {val_str}.\n"
            f"Oracle (expected) output: {oracle_output!r}\n"
            f"Agent (actual) output: {agent_output!r}\n"
            f"Ensure your program is bypassing the corrupted index properly."
        )