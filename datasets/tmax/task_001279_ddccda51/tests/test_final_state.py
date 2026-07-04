# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/auth_validator"
AGENT_PATH = "/home/user/check_perm.sh"
N_TESTS = 500

def test_agent_script_exists_and_executable():
    """Verify that the agent script exists and is executable."""
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    """Fuzz the agent script against the oracle binary to ensure bit-exact equivalence."""
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for _ in range(N_TESTS):
        length = random.randint(1, 64)
        test_input = "".join(random.choice(charset) for _ in range(length))

        oracle_proc = subprocess.run([ORACLE_PATH, test_input], capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"
        oracle_output = oracle_proc.stdout

        agent_proc = subprocess.run([AGENT_PATH, test_input], capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input: '{test_input}'. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Mismatch on input '{test_input}'.\n"
            f"Expected (Oracle): {repr(oracle_output)}\n"
            f"Got (Agent): {repr(agent_output)}"
        )