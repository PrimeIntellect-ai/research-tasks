# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_name_obfuscator"
AGENT_PATH = "/home/user/backup/name_obfuscator"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable"

def test_no_arguments_exit_code():
    # Both oracle and agent should return exit code 1 when no arguments are provided
    oracle_proc = subprocess.run([ORACLE_PATH], capture_output=True, text=True)
    agent_proc = subprocess.run([AGENT_PATH], capture_output=True, text=True)

    assert agent_proc.returncode == 1, f"Expected exit code 1 with no arguments, got {agent_proc.returncode}"
    # Optionally check if they match exactly, but the rubric only specifies exit code 1.

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file at {ORACLE_PATH} is not executable"

    random.seed(42)
    charset = string.ascii_letters + string.digits + ".-/"

    N = 1000
    for i in range(N):
        length = random.randint(1, 200)
        fuzz_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run([ORACLE_PATH, fuzz_input], capture_output=True, text=True)
        oracle_out = oracle_proc.stdout
        oracle_code = oracle_proc.returncode

        # Run agent
        agent_proc = subprocess.run([AGENT_PATH, fuzz_input], capture_output=True, text=True)
        agent_out = agent_proc.stdout
        agent_code = agent_proc.returncode

        assert agent_code == oracle_code, (
            f"Exit code mismatch on input: {repr(fuzz_input)}\n"
            f"Oracle exit code: {oracle_code}\n"
            f"Agent exit code: {agent_code}"
        )

        assert agent_out == oracle_out, (
            f"Output mismatch on input: {repr(fuzz_input)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )