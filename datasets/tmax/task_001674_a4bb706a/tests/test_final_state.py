# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/home/user/oracle"
    agent_path = "/home/user/fixed_parser.py"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary at {oracle_path} is not executable"

    assert os.path.isfile(agent_path), f"Agent script not found at {agent_path}"

    random.seed(42)

    # Characters to bias towards (using escaped null byte since actual null bytes cannot be passed in CLI args)
    edge_cases = [':', '[', ']', '\\x00']
    base_chars = list(string.printable)

    def generate_input():
        length = random.randint(1, 100)
        chars = []
        for _ in range(length):
            if random.random() < 0.2:
                chars.append(random.choice(edge_cases))
            else:
                chars.append(random.choice(base_chars))
        return "".join(chars)

    N = 5000
    for i in range(N):
        inp_str = generate_input()

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, inp_str],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_res.stdout
            oracle_err = oracle_res.stderr
            oracle_code = oracle_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {inp_str!r}")
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input {inp_str!r}: {e}")

        # Run agent
        try:
            agent_res = subprocess.run(
                ["/usr/bin/python3", agent_path, inp_str],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_res.stdout
            agent_err = agent_res.stderr
            agent_code = agent_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {inp_str!r}")
        except Exception as e:
            pytest.fail(f"Agent script failed to run on input {inp_str!r}: {e}")

        assert oracle_code == agent_code, (
            f"Return code mismatch on input {inp_str!r}.\n"
            f"Oracle: {oracle_code}\nAgent: {agent_code}\n"
            f"Oracle stderr: {oracle_err!r}\nAgent stderr: {agent_err!r}"
        )

        assert oracle_out == agent_out, (
            f"Output mismatch on input {inp_str!r}.\n"
            f"Oracle output: {oracle_out!r}\nAgent output: {agent_out!r}"
        )