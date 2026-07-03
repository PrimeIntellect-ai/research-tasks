# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fixed_hash_exists_and_executable():
    path = "/home/user/fixed_hash"
    assert os.path.isfile(path), f"The target executable {path} does not exist."
    assert os.access(path, os.X_OK), f"The target executable {path} is not marked as executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/hash_oracle"
    agent_path = "/home/user/fixed_hash"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent program {agent_path} missing."

    random.seed(1337)
    N = 10000

    for i in range(N):
        length = random.randint(0, 8192)
        data = random.randbytes(length)

        oracle_proc = subprocess.run([oracle_path], input=data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with length {length}."
        assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with length {length}."

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on iteration {i} (input length {length}).\n"
            f"Expected (Oracle): {oracle_proc.stdout!r}\n"
            f"Got (Agent): {agent_proc.stdout!r}"
        )