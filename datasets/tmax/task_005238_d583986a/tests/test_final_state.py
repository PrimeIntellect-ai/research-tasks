# test_final_state.py

import os
import subprocess
import random
import struct
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_processor"
AGENT_PATH = "/home/user/replacement.py"
N_ITERATIONS = 1000

def generate_random_chunk():
    # 0: Valid float32
    # 1: Specific NaN (0xFFFFFFFF)
    # 2: Other NaN
    # 3: Inf
    # 4: -Inf
    # 5: Random bytes
    choice = random.randint(0, 5)
    if choice == 0:
        return struct.pack('<f', random.uniform(-1000.0, 1000.0))
    elif choice == 1:
        return b'\xff\xff\xff\xff'
    elif choice == 2:
        return struct.pack('<f', float('nan'))
    elif choice == 3:
        return struct.pack('<f', float('inf'))
    elif choice == 4:
        return struct.pack('<f', float('-inf'))
    else:
        return bytes([random.randint(0, 255) for _ in range(4)])

def test_replacement_script_exists():
    assert os.path.exists(AGENT_PATH), f"Replacement script not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Replacement script at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "input.bin")

        for i in range(N_ITERATIONS):
            num_chunks = random.randint(1, 256)
            data = b"".join(generate_random_chunk() for _ in range(num_chunks))

            with open(input_file, "wb") as f:
                f.write(data)

            # Run oracle
            try:
                oracle_result = subprocess.run(
                    [ORACLE_PATH, input_file],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                oracle_stdout = oracle_result.stdout.strip()
            except subprocess.TimeoutExpired:
                pytest.fail(f"Oracle timed out on input iteration {i}")

            # Run agent
            try:
                agent_result = subprocess.run(
                    [AGENT_PATH, input_file],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                agent_stdout = agent_result.stdout.strip()
            except subprocess.TimeoutExpired:
                pytest.fail(f"Agent script timed out on input iteration {i}")

            assert agent_result.returncode == oracle_result.returncode, \
                f"Return code mismatch on iteration {i}. Oracle: {oracle_result.returncode}, Agent: {agent_result.returncode}"

            assert agent_stdout == oracle_stdout, \
                f"Output mismatch on iteration {i}!\nInput hex: {data.hex()}\nOracle output: {oracle_stdout}\nAgent output: {agent_stdout}"