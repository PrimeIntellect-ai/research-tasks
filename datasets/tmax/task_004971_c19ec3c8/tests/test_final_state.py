# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/custom_decompress.py"
ORACLE_BINARY = "/app/oracle_decompress"
NUM_FUZZ_TESTS = 200

def generate_rle_data(min_len=10, max_len=50000):
    target_length = random.randint(min_len, max_len)
    data = bytearray()
    while len(data) < target_length:
        chunk_type = random.choice(['repeat', 'literal'])
        n = random.randint(0, 127)
        if chunk_type == 'repeat':
            data.append(0x80 | n)
            data.append(random.randint(0, 255))
        else:
            data.append(n)
            for _ in range(n + 1):
                data.append(random.randint(0, 255))
    return bytes(data)

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"Path {AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary {ORACLE_BINARY} is not executable"

    random.seed(42)

    for i in range(NUM_FUZZ_TESTS):
        input_data = generate_rle_data()

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_BINARY],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on fuzz input {i}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on fuzz input {i}")

        assert agent_proc.returncode == 0, (
            f"Agent script failed with return code {agent_proc.returncode} on fuzz input {i}.\n"
            f"Stderr: {agent_proc.stderr.decode(errors='replace')}"
        )

        assert agent_output == oracle_output, (
            f"Output mismatch on fuzz input {i}.\n"
            f"Input length: {len(input_data)} bytes.\n"
            f"Oracle output length: {len(oracle_output)} bytes.\n"
            f"Agent output length: {len(agent_output)} bytes."
        )