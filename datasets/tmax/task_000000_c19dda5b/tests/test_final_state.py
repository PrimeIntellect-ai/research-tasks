# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fixed_parser_exists_and_executable():
    path = "/home/user/fixed_parser"
    assert os.path.exists(path), f"Expected file {path} does not exist. Did you compile your fixed C program?"
    assert os.path.isfile(path), f"Expected {path} to be a file."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_oracle_parser_exists():
    path = "/app/oracle_parser"
    assert os.path.exists(path), f"Reference oracle {path} is missing."
    assert os.path.isfile(path), f"Reference oracle {path} is not a file."
    assert os.access(path, os.X_OK), f"Reference oracle {path} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/fixed_parser"
    oracle_bin = "/app/oracle_parser"

    if not os.path.exists(agent_bin) or not os.access(agent_bin, os.X_OK):
        pytest.fail(f"Cannot run fuzzing: {agent_bin} is missing or not executable.")
    if not os.path.exists(oracle_bin) or not os.access(oracle_bin, os.X_OK):
        pytest.fail(f"Cannot run fuzzing: {oracle_bin} is missing or not executable.")

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    N = 5000

    for i in range(N):
        length = random.randint(10, 256)
        test_input = "".join(random.choices(charset, k=length))

        try:
            oracle_proc = subprocess.run(
                [oracle_bin, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input!r}")
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input: {test_input!r}. Error: {e}")

        try:
            agent_proc = subprocess.run(
                [agent_bin, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Your parser timed out on input: {test_input!r}")
        except Exception as e:
            pytest.fail(f"Your parser failed to run on input: {test_input!r}. Error: {e}")

        assert agent_out == oracle_out, (
            f"Output mismatch on input: {test_input!r}\n"
            f"Expected (Oracle): {oracle_out!r}\n"
            f"Got (Agent): {agent_out!r}"
        )