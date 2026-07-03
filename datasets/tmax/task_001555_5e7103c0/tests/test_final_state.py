# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_aggregator"
    agent_path = "/home/user/aggregator/aggregator_fixed"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    N = 1000
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    min_length = 5
    max_length = 128

    random.seed(42)

    lines = []
    for _ in range(N):
        length = random.randint(min_length, max_length)
        payload = "".join(random.choice(charset) for _ in range(length))
        lines.append(payload)

    input_data = ("\n".join(lines) + "\n").encode('utf-8')

    try:
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True,
            timeout=10,
            check=True
        )
        oracle_out = oracle_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed: {e.stderr.decode(errors='replace')}")

    try:
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True,
            timeout=10,
            check=True
        )
        agent_out = agent_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out. This likely indicates a deadlock under high contention.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program failed with exit code {e.returncode}: {e.stderr.decode(errors='replace')}")

    if oracle_out != agent_out:
        # Find the first differing byte to provide a helpful error message
        min_len = min(len(oracle_out), len(agent_out))
        diff_idx = -1
        for i in range(min_len):
            if oracle_out[i] != agent_out[i]:
                diff_idx = i
                break

        if diff_idx == -1:
            diff_idx = min_len

        context_start = max(0, diff_idx - 16)
        context_end = min(max(len(oracle_out), len(agent_out)), diff_idx + 16)

        expected_context = oracle_out[context_start:context_end].hex()
        actual_context = agent_out[context_start:context_end].hex()

        pytest.fail(
            f"Output mismatch detected!\n"
            f"Expected output length: {len(oracle_out)} bytes\n"
            f"Actual output length: {len(agent_out)} bytes\n"
            f"First difference at byte index {diff_idx}.\n"
            f"Expected context (hex) around diff: {expected_context}\n"
            f"Actual context (hex) around diff:   {actual_context}\n"
            f"Ensure your serialization logic matches the required magic bytes and endianness."
        )