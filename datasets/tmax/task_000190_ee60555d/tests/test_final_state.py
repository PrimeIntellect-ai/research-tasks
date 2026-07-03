# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/bin/wal_tracker"
AGENT_PATH = "/home/user/my_tracker"
NUM_TESTS = 200

def generate_fuzz_input(seed):
    random.seed(seed)
    length = random.randint(0, 1024)

    # 10% chance of having a non-multiple of 8 trailing bytes
    if random.random() >= 0.1:
        length = (length // 8) * 8

    data = bytearray()
    for i in range(length):
        if i % 8 == 0:
            # 80% chance of op_type being 0x01, 0x02, or 0x03
            if random.random() < 0.8:
                data.append(random.choice([0x01, 0x02, 0x03]))
            else:
                data.append(random.randint(0, 255))
        else:
            data.append(random.randint(0, 255))

    return bytes(data)

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"

    for i in range(NUM_TESTS):
        input_data = generate_fuzz_input(seed=42 + i)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on test {i} (seed {42+i}).\n"
            f"Input length: {len(input_data)} bytes\n"
            f"Oracle exit code: {oracle_proc.returncode}\n"
            f"Agent exit code: {agent_proc.returncode}\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}\n"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on test {i} (seed {42+i}).\n"
            f"Input length: {len(input_data)} bytes\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}\n"
        )