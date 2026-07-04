# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fixed_binary_exists_and_executable():
    fixed_bin_path = "/home/user/fxhash_fixed"
    assert os.path.exists(fixed_bin_path), f"Fixed binary {fixed_bin_path} is missing."
    assert os.path.isfile(fixed_bin_path), f"{fixed_bin_path} is not a file."
    assert os.access(fixed_bin_path, os.X_OK), f"Fixed binary {fixed_bin_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/fxhash_legacy"
    agent_path = "/home/user/fxhash_fixed"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} missing."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} missing."

    random.seed(42)
    N = 1000
    min_len = 100
    max_len = 100000

    for i in range(N):
        length = random.randint(min_len, max_len)
        test_input = bytearray(random.getrandbits(8) for _ in range(length))

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input of length {length}. Stderr: {e.stderr.decode('utf-8', errors='replace')}")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=test_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=True
            )
            agent_out = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on input of length {length}. Stderr: {e.stderr.decode('utf-8', errors='replace')}")

        assert agent_out == oracle_out, (
            f"Output mismatch on random input {i} (length {length}).\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )