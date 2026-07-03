# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_path = "/app/repo/parser"

    assert os.path.isfile(oracle_path), f"Oracle executable {oracle_path} does not exist."
    assert os.access(oracle_path, os.X_OK), f"Oracle executable {oracle_path} is not executable."

    assert os.path.isfile(agent_path), f"Agent executable {agent_path} does not exist."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

    # Set up random generator with a fixed seed for reproducibility
    rng = random.Random(42)
    charset = string.ascii_letters + string.digits + "-"

    num_tests = 500
    for i in range(num_tests):
        length = rng.randint(10, 60)
        test_input = "".join(rng.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_res.stdout
            oracle_err = oracle_res.stderr
            oracle_code = oracle_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_path, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_res.stdout
            agent_err = agent_res.stderr
            agent_code = agent_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent's program timed out on input: {test_input}")

        # Compare return codes (optional but good practice)
        assert agent_code == oracle_code, (
            f"Return code mismatch on input: {test_input}\n"
            f"Oracle returned {oracle_code}, Agent returned {agent_code}\n"
            f"Oracle stderr: {oracle_err}\nAgent stderr: {agent_err}"
        )

        # Compare outputs
        assert agent_out == oracle_out, (
            f"Output mismatch on input: {test_input}\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}\n"
        )