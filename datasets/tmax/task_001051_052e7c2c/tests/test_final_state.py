# test_final_state.py

import os
import struct
import random
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_aggregator"
AGENT_PATH = "/home/user/log_cleaner"

def generate_input(num_records):
    """
    Generates a binary blob stream of 24-byte structs:
    uint64_t timestamp, uint32_t metric_id, uint32_t is_retry, double value
    """
    records = []
    ts_per_metric = {1: 1000000, 2: 1000000, 3: 1000000, 4: 1000000}

    for _ in range(num_records):
        metric_id = random.choice([1, 2, 3, 4])

        # Monotonically increasing per metric, with occasional exact duplicates
        if random.random() < 0.2:
            ts = ts_per_metric[metric_id]
        else:
            ts_per_metric[metric_id] += random.randint(1, 5)
            ts = ts_per_metric[metric_id]

        is_retry = random.choice([0, 1, 2])
        value = random.uniform(-1000.0, 1000.0)

        records.append(struct.pack('<QIId', ts, metric_id, is_retry, value))

    return b''.join(records)

def test_fuzz_equivalence():
    """
    Fuzzes the agent's C implementation against the oracle binary.
    """
    assert os.path.exists(AGENT_PATH), f"Agent program not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program at {AGENT_PATH} is not executable"

    random.seed(42)

    # We use N=100 iterations with varying sizes to keep test execution time reasonable
    # while still providing robust fuzzing coverage.
    for i in range(100):
        # Varying from small streams to larger streams
        num_records = random.randint(10, 5000)
        input_data = generate_input(num_records)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr.decode('utf-8', errors='ignore')}"

        if oracle_proc.stdout != agent_proc.stdout:
            # If there's a mismatch, we provide a clear error message
            oracle_len = len(oracle_proc.stdout)
            agent_len = len(agent_proc.stdout)
            pytest.fail(
                f"Output mismatch on fuzz iteration {i} with {num_records} records.\n"
                f"Oracle output length: {oracle_len} bytes\n"
                f"Agent output length: {agent_len} bytes\n"
                f"The agent's output does not exactly match the legacy binary's output."
            )