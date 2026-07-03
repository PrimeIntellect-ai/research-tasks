# test_final_state.py
import os
import time
import subprocess
import struct
import random
import pytest

AGENT_BIN = "/home/user/workspace/build/fast_sorter"
ORACLE_BIN = "/app/legacy_sorter"
TEST_FILE = "/tmp/test_data.bin"
ORACLE_OUT = "/tmp/oracle.out"
AGENT_OUT = "/tmp/agent.out"

def generate_test_data(num_records):
    """Generate random records quickly by writing in chunks."""
    labels = [f"label_{i}".encode('ascii').ljust(16, b'\0') for i in range(100)]
    chunk_size = 10000

    with open(TEST_FILE, "wb") as f:
        for chunk_idx in range(num_records // chunk_size):
            base_id = chunk_idx * chunk_size
            chunk = b"".join(
                struct.pack("<Qd16s", base_id + i, random.random(), labels[(base_id + i) % 100])
                for i in range(chunk_size)
            )
            f.write(chunk)

def test_fast_sorter_metric():
    assert os.path.exists(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable"

    # Generate test data (~96MB)
    num_records = 3000000
    generate_test_data(num_records)

    # Run oracle
    t0 = time.time()
    with open(ORACLE_OUT, "wb") as f:
        subprocess.run([ORACLE_BIN, TEST_FILE], stdout=f, check=True)
    oracle_time = time.time() - t0

    # Run agent
    t0 = time.time()
    with open(AGENT_OUT, "wb") as f:
        subprocess.run([AGENT_BIN, TEST_FILE], stdout=f, check=True)
    agent_time = time.time() - t0

    # Verify correctness byte-for-byte in chunks to save memory
    with open(ORACLE_OUT, "rb") as f1, open(AGENT_OUT, "rb") as f2:
        chunk_size = 8 * 1024 * 1024
        offset = 0
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)
            assert chunk1 == chunk2, f"Agent output differs from Oracle output starting at byte offset {offset}."
            if not chunk1:
                break
            offset += len(chunk1)

    # Verify speedup
    speedup = oracle_time / agent_time
    assert speedup >= 1.5, (
        f"Speedup is {speedup:.2f}x, which is below the threshold of 1.5x. "
        f"Oracle time: {oracle_time:.2f}s, Agent time: {agent_time:.2f}s."
    )