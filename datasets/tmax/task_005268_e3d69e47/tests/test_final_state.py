# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_BINARY = "/home/user/transformer"
ORACLE_BINARY = "/app/oracle_transformer"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BINARY), f"Agent binary not found at {AGENT_BINARY}"
    assert os.path.isfile(AGENT_BINARY), f"Path {AGENT_BINARY} is not a file"
    assert os.access(AGENT_BINARY, os.X_OK), f"Agent binary {AGENT_BINARY} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary {ORACLE_BINARY} is not executable"

    random.seed(42)
    num_iterations = 50

    for i in range(num_iterations):
        # Generate random length between 0 and 100,000
        length = random.randint(0, 100000)

        # Generate random bytes
        # Using random.randbytes if available, otherwise os.urandom for speed, but random with fixed seed is required for reproducibility
        # Since we need reproducible inputs based on seed, we use random.getrandbits or similar.
        # Actually, standard library `random.randbytes` is available in Python 3.9+.
        input_data = random.randbytes(length)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_BINARY],
                input=input_data,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i} with length {length}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i} with length {length}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_BINARY],
                input=input_data,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on iteration {i} with length {length}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on iteration {i} with length {length}")

        # Compare outputs
        if oracle_output != agent_output:
            # To avoid massive output in terminal, just show lengths and a snippet
            mismatch_msg = (
                f"Output mismatch on iteration {i} with input length {length}.\n"
                f"Oracle output length: {len(oracle_output)}\n"
                f"Agent output length: {len(agent_output)}\n"
            )
            assert oracle_output == agent_output, mismatch_msg