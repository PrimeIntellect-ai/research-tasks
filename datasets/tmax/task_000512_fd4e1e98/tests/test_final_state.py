# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/legacy_archiver"
AGENT_PATH = "/home/user/archiver"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    # Use a fixed seed for reproducibility of sizes
    rng = random.Random(42)

    for i in range(100):
        # Generate random size between 0 and 5 MB
        size = rng.randint(0, 5 * 1024 * 1024)

        # The truth specifies data generated via /dev/urandom
        input_data = os.urandom(size)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on iteration {i} (input size {size}). "
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )

        if oracle_proc.stdout != agent_proc.stdout:
            mismatch_len = min(len(oracle_proc.stdout), len(agent_proc.stdout))
            diff_idx = -1
            for j in range(mismatch_len):
                if oracle_proc.stdout[j] != agent_proc.stdout[j]:
                    diff_idx = j
                    break
            if diff_idx == -1:
                diff_idx = mismatch_len

            pytest.fail(
                f"Stdout mismatch on iteration {i} (input size {size}).\n"
                f"Oracle output length: {len(oracle_proc.stdout)}\n"
                f"Agent output length: {len(agent_proc.stdout)}\n"
                f"First differing byte index: {diff_idx}"
            )