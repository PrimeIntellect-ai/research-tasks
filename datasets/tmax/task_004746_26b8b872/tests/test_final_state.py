# test_final_state.py

import os
import random
import struct
import subprocess
import tempfile
import pytest

def test_bad_commit_file():
    bad_commit_path = "/home/user/bad_commit.txt"
    assert os.path.exists(bad_commit_path), f"{bad_commit_path} does not exist."
    with open(bad_commit_path, "r") as f:
        content = f.read().strip()
    assert len(content) == 40, f"Expected 40-character commit hash in {bad_commit_path}, got {len(content)} characters."
    # Check if it's hex
    try:
        int(content, 16)
    except ValueError:
        pytest.fail(f"Commit hash {content} is not a valid hex string.")

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_analyzer"
    agent_path = "/home/user/timeline_analyzer/analyzer"

    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}. Did you compile it?"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable."

    random.seed(42)

    for i in range(1000):
        size = random.randint(50, 10000)
        data = bytearray()

        while len(data) < size:
            is_malformed = random.random() < 0.3
            frame_type = random.randint(0, 255)
            timestamp = random.randint(0, 0xFFFFFFFF)

            remaining = size - len(data)
            if remaining < 7:
                data += bytearray(random.getrandbits(8) for _ in range(remaining))
                break

            if is_malformed:
                # Length exceeds remaining bytes
                length = random.randint(remaining - 6, 0xFFFF)
            else:
                max_len = remaining - 7
                length = random.randint(0, min(256, max_len))

            # Assume little-endian for the struct
            data += struct.pack("<B I H", frame_type, timestamp, length)
            if not is_malformed:
                data += bytearray(random.getrandbits(8) for _ in range(length))
            else:
                # Add some random bytes but not enough to fulfill the length
                add_len = random.randint(0, remaining - 7)
                data += bytearray(random.getrandbits(8) for _ in range(add_len))
                break

        data = data[:size]

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
            f_name = f.name

        try:
            oracle_proc = subprocess.run([oracle_path, "-f", f_name], capture_output=True, timeout=5)
            agent_proc = subprocess.run([agent_path, "-f", f_name], capture_output=True, timeout=5)

            assert oracle_proc.stdout == agent_proc.stdout, (
                f"Output mismatch on iteration {i}.\n"
                f"Input file size: {len(data)} bytes\n"
                f"Oracle output:\n{oracle_proc.stdout.decode('utf-8', errors='replace')}\n"
                f"Agent output:\n{agent_proc.stdout.decode('utf-8', errors='replace')}\n"
            )
        finally:
            os.remove(f_name)