# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/legacy_transform"
AGENT_PATH = "/home/user/new_transform"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"{ORACLE_PATH} is not executable"

    random.seed(42)
    N = 50

    for i in range(N):
        size = random.randint(100, 10000)
        input_floats = [random.uniform(-1000.0, 1000.0) for _ in range(size)]
        input_str = " ".join(f"{x:.6f}" for x in input_floats) + "\n"
        input_bytes = input_str.encode('utf-8')

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"
        oracle_out = oracle_proc.stdout.decode('utf-8')

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        assert agent_proc.returncode == 0, f"Agent failed on iteration {i} with stderr: {agent_proc.stderr.decode('utf-8')}"
        agent_out = agent_proc.stdout.decode('utf-8')

        if oracle_out != agent_out:
            err_msg = (
                f"Mismatch on iteration {i} with input size {size}.\n"
                f"Input sample: {input_str[:100]}...\n"
                f"Oracle output sample: {oracle_out[:100]}...\n"
                f"Agent output sample: {agent_out[:100]}...\n"
            )
            pytest.fail(err_msg)