# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_validator"
AGENT_SCRIPT = "/home/user/payload_generator.py"
NUM_TESTS = 10000

def test_payload_generator_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} is not executable"

    # Character set: Alphanumeric + standard punctuation
    charset = string.ascii_letters + string.digits + "!@#$%^&*"

    random.seed(42)  # Fixed seed for reproducibility

    # We will test a subset if 10000 is too slow, but we aim for 10000 as requested.
    # To avoid test timeout, we might sample a smaller number if it takes too long, 
    # but let's stick to 1000 to ensure it completes within a reasonable time in standard CI,
    # or just 10000 as specified. We'll use 10000.

    inputs = []
    for _ in range(NUM_TESTS):
        length = random.randint(8, 128)
        inputs.append("".join(random.choices(charset, k=length)))

    for i, test_input in enumerate(inputs):
        # Run Oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_input],
            capture_output=True,
            text=True
        )
        oracle_output = oracle_proc.stdout.strip()

        # Run Agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT, test_input],
            capture_output=True,
            text=True
        )
        agent_output = agent_proc.stdout.strip()

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"
        assert agent_proc.returncode == 0, f"Agent script failed on input: {test_input}\nError: {agent_proc.stderr}"

        assert agent_output == oracle_output, (
            f"Mismatch on test {i+1}/{NUM_TESTS}\n"
            f"Input: {test_input}\n"
            f"Oracle Output: {oracle_output}\n"
            f"Agent Output : {agent_output}"
        )