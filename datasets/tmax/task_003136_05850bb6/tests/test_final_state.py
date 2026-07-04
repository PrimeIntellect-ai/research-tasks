# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/router.sh"
ORACLE_BINARY = "/app/oracle_router"

def test_script_exists_and_executable():
    """Verify that the student's script exists and is executable."""
    assert os.path.isfile(AGENT_SCRIPT), f"Script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Script at {AGENT_SCRIPT} is not executable"

def generate_valid_input():
    """Generates a valid comma-separated string with exactly 5 fields."""
    fields = []
    for _ in range(5):
        length = random.randint(3, 10)
        field = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        fields.append(field)
    return ",".join(fields)

def generate_malformed_input():
    """Generates an invalid comma-separated string (not 5 fields)."""
    num_fields = random.choice([1, 2, 3, 4, 6, 7, 8])
    fields = []
    for _ in range(num_fields):
        length = random.randint(3, 10)
        field = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        fields.append(field)
    return ",".join(fields)

def test_fuzz_equivalence():
    """Fuzz the agent script against the oracle binary."""
    assert os.path.isfile(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary at {ORACLE_BINARY} is not executable"

    random.seed(42)
    num_tests = 1000

    for i in range(num_tests):
        # 5% malformed inputs
        if random.random() < 0.05:
            test_input = generate_malformed_input()
        else:
            test_input = generate_valid_input()

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_BINARY, test_input],
            capture_output=True,
            text=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT, test_input],
            capture_output=True,
            text=True
        )

        # Check exit code
        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input: '{test_input}'\n"
            f"Expected: {oracle_proc.returncode}, Got: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        # Check stdout
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input: '{test_input}'\n"
            f"Expected stdout:\n{oracle_proc.stdout}\n"
            f"Got stdout:\n{agent_proc.stdout}"
        )