# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_checker"
AGENT_PATH = "/home/user/policy_check"
NUM_ITERATIONS = 1000

def test_agent_executable_exists():
    """Ensure the student's compiled Go program exists and is executable."""
    assert os.path.exists(AGENT_PATH), f"Compiled binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"File {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent program to ensure bit-exact equivalence."""
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    # Use a fixed seed for reproducibility
    random.seed(42)

    hex_chars = "0123456789ABCDEF"

    for _ in range(NUM_ITERATIONS):
        # Generate a random 12-character uppercase hex string
        test_input = "".join(random.choices(hex_chars, k=12))

        # Run oracle
        oracle_result = subprocess.run(
            [ORACLE_PATH, test_input],
            capture_output=True,
            text=True,
            timeout=2
        )

        # Run agent
        agent_result = subprocess.run(
            [AGENT_PATH, test_input],
            capture_output=True,
            text=True,
            timeout=2
        )

        # Assert return codes match (or at least agent succeeds)
        # The oracle returns 0 for valid 12-char inputs.
        assert agent_result.returncode == 0, f"Agent failed on input {test_input} with stderr: {agent_result.stderr}"

        # Assert exact output match
        oracle_stdout = oracle_result.stdout
        agent_stdout = agent_result.stdout

        assert agent_stdout == oracle_stdout, (
            f"Output mismatch on input {test_input}.\n"
            f"Expected (Oracle): {repr(oracle_stdout)}\n"
            f"Got (Agent): {repr(agent_stdout)}"
        )