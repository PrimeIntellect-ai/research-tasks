# test_final_state.py

import os
import subprocess
import random
import pytest

def test_decryptor_fuzz_equivalence():
    agent_path = "/home/user/decryptor"
    oracle_path = "/app/.hidden/reference_decryptor"

    assert os.path.exists(agent_path), f"Agent decryptor not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent decryptor is not executable at {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle decryptor not found at {oracle_path}"

    random.seed(42)

    for i in range(1000):
        length = random.randint(16, 1024)
        test_input = bytes(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

        agent_proc = subprocess.run(
            [agent_path],
            input=test_input,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent decryptor failed (return code {agent_proc.returncode}) on input {i}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on input {i} (length {length}).\n"
                f"Input (hex): {test_input.hex()[:100]}...\n"
                f"Expected output (hex): {oracle_proc.stdout.hex()[:100]}...\n"
                f"Actual output (hex): {agent_proc.stdout.hex()[:100]}..."
            )