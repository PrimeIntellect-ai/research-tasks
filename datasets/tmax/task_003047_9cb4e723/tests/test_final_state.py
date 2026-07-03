# test_final_state.py

import os
import subprocess
import random
import base64
import string
import pytest

ORACLE_PATH = "/opt/oracle/worker_oracle"
AGENT_PATH = "/home/user/fixed_worker"
NUM_FUZZ_INPUTS = 1000

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        length = random.randint(1, 2000)
        raw_bytes = bytes(random.getrandbits(8) for _ in range(length))
        b64 = base64.b64encode(raw_bytes).decode('ascii')

        # Mutate some inputs
        if random.random() < 0.5:
            mutation_type = random.choice(['remove_padding', 'add_invalid', 'truncate'])
            if mutation_type == 'remove_padding':
                b64 = b64.rstrip('=')
            elif mutation_type == 'add_invalid':
                idx = random.randint(0, len(b64))
                invalid_char = random.choice(['!', '@', '\xff', '?', '-', '*'])
                b64 = b64[:idx] + invalid_char + b64[idx:]
            elif mutation_type == 'truncate':
                if len(b64) > 0:
                    b64 = b64[:-1]

        inputs.append(b64)
    return inputs

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} is missing."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    inputs = generate_fuzz_inputs(NUM_FUZZ_INPUTS)
    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data.encode('utf-8', errors='surrogateescape'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Run agent
    agent_proc = subprocess.run(
        [AGENT_PATH],
        input=input_data.encode('utf-8', errors='surrogateescape'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    assert agent_proc.returncode == oracle_proc.returncode, "Agent binary exit code does not match oracle."
    assert agent_proc.stdout == oracle_proc.stdout, "Agent binary stdout does not match oracle on fuzz inputs."

def test_no_memory_leaks():
    # Run under valgrind to check for memory leaks
    inputs = generate_fuzz_inputs(100) # subset for speed
    input_data = "\n".join(inputs) + "\n"

    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=42",
        AGENT_PATH
    ]

    try:
        proc = subprocess.run(
            valgrind_cmd,
            input=input_data.encode('utf-8', errors='surrogateescape'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert proc.returncode != 42, "Valgrind reported memory leaks or errors."
        assert proc.returncode == 0, f"Agent binary crashed under valgrind with exit code {proc.returncode}."
    except FileNotFoundError:
        pytest.skip("Valgrind not found, skipping memory leak test.")