# test_final_state.py

import os
import random
import subprocess
import struct
import pytest

ORACLE_PATH = "/app/oracle_parser"
AGENT_PATH = "/home/user/config_parser"
NUM_TESTS = 500

def generate_random_chunk():
    num_chars = random.randint(0, 2000)
    chars = []
    for _ in range(num_chars):
        cp = random.randint(0, 0x10FFFF)
        # Exclude surrogate range
        if 0xD800 <= cp <= 0xDFFF:
            cp = random.randint(0, 0xD7FF)
        chars.append(chr(cp))

    # Encode to utf-16le
    utf16_bytes = "".join(chars).encode("utf-16le")
    header = struct.pack("<I", num_chars)
    return header + utf16_bytes

def generate_input(truncate=False):
    num_chunks = random.randint(0, 50)
    data = b"".join(generate_random_chunk() for _ in range(num_chunks))
    if truncate and len(data) > 0:
        truncate_len = random.randint(0, len(data) - 1)
        data = data[:truncate_len]
    return data

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        is_truncated = (i % 10 == 0) # 10% truncated
        input_data = generate_input(truncate=is_truncated)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on test {i} (truncated={is_truncated}). "
            f"Expected {oracle_proc.returncode}, got {agent_proc.returncode}."
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on test {i} (truncated={is_truncated}). "
            f"Input length: {len(input_data)} bytes."
        )