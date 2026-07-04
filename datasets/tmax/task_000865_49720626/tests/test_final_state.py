# test_final_state.py

import os
import random
import subprocess
import string
import struct
import pytest

ORACLE_PATH = "/app/token_validator"
AGENT_PATH = "/home/user/validator"
NUM_TESTS = 1000

def calc_hash(payload: bytes) -> int:
    hash_val = 0x12345678
    for b in payload:
        hash_val ^= b
        hash_val = ((hash_val << 5) & 0xFFFFFFFF) | (hash_val >> 27)
        hash_val = (hash_val + 0x5A5A5A5A) & 0xFFFFFFFF
    return hash_val

def generate_inputs(seed=42):
    random.seed(seed)
    inputs = []

    # 20% invalid hex characters
    for _ in range(int(NUM_TESTS * 0.2)):
        length = random.randint(1, 100)
        chars = [random.choice(string.printable) for _ in range(length)]
        # ensure at least one invalid hex char
        invalid_chars = set(string.printable) - set(string.hexdigits) - set(' \t\n\r')
        if invalid_chars:
            chars[random.randint(0, length - 1)] = random.choice(list(invalid_chars))
        inputs.append("".join(chars).encode('utf-8'))

    # 20% valid hex strings of length < 10
    for _ in range(int(NUM_TESTS * 0.2)):
        length = random.randint(0, 9)
        chars = [random.choice(string.hexdigits) for _ in range(length)]
        inputs.append("".join(chars).encode('utf-8'))

    # 30% valid hex strings of random length (10 to 512 chars) with random checksums
    for _ in range(int(NUM_TESTS * 0.3)):
        length = random.randint(10, 512)
        # ensure even length if we want valid hex processing up to checksum
        if length % 2 != 0:
            length += 1
        chars = [random.choice(string.hexdigits) for _ in range(length)]
        inputs.append("".join(chars).encode('utf-8'))

    # 30% perfectly crafted valid tokens
    for _ in range(int(NUM_TESTS * 0.3)):
        payload_len = random.randint(1, 250)
        payload = bytes([random.randint(0, 255) for _ in range(payload_len)])
        checksum = calc_hash(payload)
        token_bytes = payload + struct.pack("<I", checksum)
        inputs.append(token_bytes.hex().encode('utf-8'))

    random.shuffle(inputs)
    return inputs

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    inputs = generate_inputs()

    for idx, inp in enumerate(inputs):
        oracle_proc = subprocess.run([ORACLE_PATH], input=inp, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=inp, capture_output=True)

        err_msg = (
            f"Mismatch on input #{idx}!\n"
            f"Input (hex): {inp.hex()}\n"
            f"Oracle stdout: {oracle_proc.stdout}\n"
            f"Agent stdout: {agent_proc.stdout}\n"
            f"Oracle stderr: {oracle_proc.stderr}\n"
            f"Agent stderr: {agent_proc.stderr}\n"
            f"Oracle exit code: {oracle_proc.returncode}\n"
            f"Agent exit code: {agent_proc.returncode}\n"
        )

        assert oracle_proc.returncode == agent_proc.returncode, err_msg
        assert oracle_proc.stdout == agent_proc.stdout, err_msg
        assert oracle_proc.stderr == agent_proc.stderr, err_msg