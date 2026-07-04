# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/legacy_token_gen"
AGENT_PATH = "/home/user/my_token_gen"

def test_agent_program_exists_and_executable():
    """Test that the agent's token generator script exists and is executable."""
    assert os.path.exists(AGENT_PATH), f"Agent program missing at {AGENT_PATH}. You must create your script here."
    assert os.path.isfile(AGENT_PATH), f"Agent path {AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program at {AGENT_PATH} is not marked as executable."

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent's program to ensure bit-exact equivalence."""
    assert os.path.exists(ORACLE_PATH), f"Oracle program missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program at {ORACLE_PATH} is not executable"

    # Fixed seed for reproducible tests
    random.seed(42)
    chars = string.ascii_letters + string.digits

    # N=50 inputs
    for i in range(50):
        # Lengths uniformly chosen between 8 and 32
        length = random.randint(8, 32)
        test_input = ''.join(random.choice(chars) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run([ORACLE_PATH, test_input], capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle program failed unexpectedly on input '{test_input}'"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent program
        agent_proc = subprocess.run([AGENT_PATH, test_input], capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent program failed on input '{test_input}'.\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        # Assert equivalence
        assert agent_output == oracle_output, (
            f"Output mismatch on fuzz iteration {i+1} for input '{test_input}'.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent):       {agent_output}"
        )