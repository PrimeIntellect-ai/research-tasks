# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_agent_files_exist():
    """Verify that the agent has created the required source and compiled binary."""
    c_path = "/home/user/hasher_rebuilt.c"
    bin_path = "/home/user/hasher_rebuilt"

    assert os.path.exists(c_path), f"Source file {c_path} is missing."
    assert os.path.exists(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent's binary to ensure exact equivalence."""
    oracle_path = "/app/legacy_hasher"
    agent_path = "/home/user/hasher_rebuilt"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} is missing."

    # Generate random inputs
    random.seed(42)
    # Exclude null bytes and carriage returns/newlines which might cause issues in argv passing
    # depending on the environment, though subprocess handles them. 
    # string.printable contains whitespace chars. We'll use letters, digits, punctuation, and space.
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    num_tests = 1000

    for _ in range(num_tests):
        length = random.randint(0, 64)
        test_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_res.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {repr(test_input)}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_path, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_res.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {repr(test_input)}")

        assert agent_res.returncode == oracle_res.returncode, (
            f"Return code mismatch on input {repr(test_input)}.\n"
            f"Oracle: {oracle_res.returncode}, Agent: {agent_res.returncode}"
        )

        assert agent_out == oracle_out, (
            f"Output mismatch on input {repr(test_input)}.\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output:  {repr(agent_out)}"
        )