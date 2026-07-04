# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_agent_binary_exists():
    path = "/home/user/token_v2"
    assert os.path.isfile(path), f"Agent binary {path} does not exist. Did you compile your code to the correct location?"
    assert os.access(path, os.X_OK), f"Agent binary {path} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/token_v2"
    oracle_bin = "/oracle/token_v2_oracle"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} missing."
    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} missing."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for _ in range(100):
        length = random.randint(5, 50)
        input_str = "".join(random.choice(charset) for _ in range(length))

        try:
            oracle_res = subprocess.run([oracle_bin, input_str], capture_output=True, text=True, timeout=2)
            oracle_out = oracle_res.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input: {input_str}")

        try:
            agent_res = subprocess.run([agent_bin, input_str], capture_output=True, text=True, timeout=2)
            agent_out = agent_res.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Your binary timed out on input: {input_str}")

        assert agent_res.returncode == oracle_res.returncode, (
            f"Return code mismatch on input '{input_str}'. "
            f"Expected {oracle_res.returncode}, got {agent_res.returncode}."
        )
        assert agent_out == oracle_out, (
            f"Output mismatch on input '{input_str}'.\n"
            f"Expected output:\n{oracle_out}\n"
            f"Got output:\n{agent_out}"
        )