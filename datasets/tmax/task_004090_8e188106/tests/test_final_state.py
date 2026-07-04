# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/.hidden/payload_decoder_oracle"
    agent_path = "/home/user/clean_decoder"

    assert os.path.exists(agent_path), f"Agent executable not found at {agent_path}"
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable"

    assert os.path.exists(oracle_path), f"Oracle executable not found at {oracle_path}"

    # Fuzzing parameters
    N = 500
    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation

    for i in range(N):
        length = random.randint(1, 64)
        input_str = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, input_str],
            capture_output=True,
            text=True,
            timeout=2
        )
        assert oracle_res.returncode == 0, f"Oracle failed on input: {input_str!r}"

        # Run agent
        agent_res = subprocess.run(
            [agent_path, input_str],
            capture_output=True,
            text=True,
            timeout=2
        )

        if agent_res.returncode != 0:
            pytest.fail(f"Agent executable failed (return code {agent_res.returncode}) on input: {input_str!r}\nStderr: {agent_res.stderr}")

        oracle_output = oracle_res.stdout.strip()
        agent_output = agent_res.stdout.strip()

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on input: {input_str!r}\n"
                f"Expected (Oracle): {oracle_output}\n"
                f"Got (Agent):       {agent_output}"
            )