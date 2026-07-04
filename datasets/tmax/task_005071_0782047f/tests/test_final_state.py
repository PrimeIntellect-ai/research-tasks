# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/ws_oracle"
AGENT_PATH = "/home/user/bin/parser"
NUM_ITERATIONS = 10000

def generate_valid_frame():
    opcode = random.choice([1, 8])
    fin = random.choice([0, 0x80])
    byte0 = fin | opcode

    mask = random.choice([0, 0x80])
    payload_len = random.randint(0, 125)
    byte1 = mask | payload_len

    frame = bytearray([byte0, byte1])

    if mask:
        mask_key = [random.randint(0, 255) for _ in range(4)]
        frame.extend(mask_key)

    payload = bytearray([random.randint(0, 255) for _ in range(payload_len)])
    frame.extend(payload)
    return bytes(frame)

def generate_valid_frames_input():
    data = bytearray()
    num_frames = random.randint(1, 10)
    for _ in range(num_frames):
        data.extend(generate_valid_frame())
    return bytes(data)

def generate_random_noise():
    length = random.randint(1, 1024)
    return bytes([random.randint(0, 255) for _ in range(length)])

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary is not executable: {AGENT_PATH}"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        if random.random() < 0.5:
            input_data = generate_valid_frames_input()
        else:
            input_data = generate_random_noise()

        if len(input_data) > 1024:
            input_data = input_data[:1024]
        if len(input_data) == 0:
            input_data = b'\x00'

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        if oracle_proc.returncode != agent_proc.returncode or oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Mismatch on iteration {i} with input {input_data.hex()}.\n"
                        f"Oracle returncode: {oracle_proc.returncode}, Agent returncode: {agent_proc.returncode}\n"
                        f"Oracle stdout: {oracle_proc.stdout!r}\n"
                        f"Agent stdout: {agent_proc.stdout!r}")