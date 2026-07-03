# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_hash_runner_exists_and_executable():
    path = "/home/user/hash_runner"
    assert os.path.isfile(path), f"Agent's program {path} does not exist."
    assert os.access(path, os.X_OK), f"Agent's program {path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/legacyhash_oracle"
    agent_path = "/home/user/hash_runner"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} does not exist."
    assert os.access(oracle_path, os.X_OK), f"Oracle program {oracle_path} is not executable."

    random.seed(42)
    printable_chars = string.printable

    for i in range(1000):
        length = random.randint(1, 256)
        test_input = "".join(random.choice(printable_chars) for _ in range(length))

        try:
            oracle_result = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {repr(test_input)}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {repr(test_input)}")

        try:
            agent_result = subprocess.run(
                [agent_path, test_input],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {repr(test_input)}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {repr(test_input)}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {repr(test_input)}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )