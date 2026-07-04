# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_random_utf8(length):
    chars = []
    for _ in range(length):
        cp = random.randint(0, 0x10FFFF)
        # Avoid surrogate halves
        if 0xD800 <= cp <= 0xDFFF:
            cp = 0x0020
        chars.append(chr(cp))
    return "".join(chars).encode('utf-8')

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_aggregator"
    agent_path = "/home/user/etl_transformer"

    assert os.path.exists(agent_path), f"Agent executable not found at {agent_path}"
    assert os.path.isfile(agent_path), f"Path {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent program at {agent_path} is not executable"

    random.seed(42)
    num_iterations = 100

    for i in range(num_iterations):
        length = random.randint(0, 5000)
        input_data = generate_random_utf8(length)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True
        )

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Iteration {i}: stdout mismatch.\n"
                f"Input length: {length} chars\n"
                f"Oracle stdout (first 200 bytes): {oracle_proc.stdout[:200]}\n"
                f"Agent stdout (first 200 bytes): {agent_proc.stdout[:200]}"
            )

        if oracle_proc.stderr != agent_proc.stderr:
            pytest.fail(
                f"Iteration {i}: stderr mismatch.\n"
                f"Input length: {length} chars\n"
                f"Oracle stderr (first 200 bytes): {oracle_proc.stderr[:200]}\n"
                f"Agent stderr (first 200 bytes): {agent_proc.stderr[:200]}"
            )

        if oracle_proc.returncode != agent_proc.returncode:
            pytest.fail(
                f"Iteration {i}: returncode mismatch.\n"
                f"Oracle returned {oracle_proc.returncode}, Agent returned {agent_proc.returncode}"
            )