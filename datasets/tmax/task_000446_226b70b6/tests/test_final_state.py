# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_PATH = "/home/user/artifact_parser"
LIB_PATH = "/app/vendor/inih-53/libinih.a"

def test_libinih_compiled():
    assert os.path.exists(LIB_PATH), f"{LIB_PATH} does not exist. Did you fix the Makefile and run make?"

def test_agent_parser_exists():
    assert os.path.exists(AGENT_PATH), f"{AGENT_PATH} does not exist. Did you compile your C program?"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable."

def generate_random_ini(length):
    chars = string.ascii_letters + string.digits + "[]=\n"
    return "".join(random.choice(chars) for _ in range(length)).encode('utf-8')

def test_fuzz_equivalence():
    random.seed(42)
    N = 1000

    for i in range(N):
        length = random.randint(10, 5000)
        input_data = generate_random_ini(length)

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH], input=input_data, capture_output=True, timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle parser timed out (this should not happen).")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH], input=input_data, capture_output=True, timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent parser timed out on iteration {i}. Input length: {length}.")

        if agent_proc.stdout != oracle_proc.stdout:
            input_preview = input_data[:200] + (b"..." if len(input_data) > 200 else b"")
            oracle_preview = oracle_proc.stdout[:200] + (b"..." if len(oracle_proc.stdout) > 200 else b"")
            agent_preview = agent_proc.stdout[:200] + (b"..." if len(agent_proc.stdout) > 200 else b"")
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input preview:\n{input_preview}\n\n"
                f"Oracle output preview:\n{oracle_preview}\n\n"
                f"Agent output preview:\n{agent_preview}\n"
            )