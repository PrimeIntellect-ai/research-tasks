# test_final_state.py
import os
import random
import subprocess
import pytest

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    for _ in range(n):
        hash_str = ''.join(random.choices("0123456789abcdef", k=8))
        port = random.randint(1, 65535)
        # 10-digit unix timestamp starting with 16 or 17
        timestamp = random.randint(1600000000, 1799999999)
        inputs.append(f"{hash_str}:{port}:{timestamp}")
    return inputs

def test_token_gen_fuzz_equivalence():
    oracle_path = "/app/audit_oracle"
    agent_path = "/home/user/token_gen"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    inputs = generate_fuzz_inputs(1000)

    for inp in inputs:
        oracle_res = subprocess.run([oracle_path, inp], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {inp}: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout

        agent_res = subprocess.run([agent_path, inp], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent program failed on input {inp}: {agent_res.stderr}"
        agent_out = agent_res.stdout

        assert oracle_out == agent_out, (
            f"Mismatch on input '{inp}'.\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output:  {repr(agent_out)}"
        )