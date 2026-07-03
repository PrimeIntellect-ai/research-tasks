# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_student_files_exist():
    """Check that the student's C source and executable exist."""
    c_source_path = "/home/user/token_gen.c"
    executable_path = "/home/user/token_gen"

    assert os.path.isfile(c_source_path), f"Student source file {c_source_path} is missing."
    assert os.path.isfile(executable_path), f"Student executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"Student executable {executable_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz test the student's program against the oracle."""
    oracle_path = "/app/oracle_token_gen"
    agent_path = "/home/user/token_gen"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary at {oracle_path} is not executable"

    random.seed(42)
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

    for i in range(1000):
        length = random.randint(3, 128)
        fuzz_input = "".join(random.choice(charset) for _ in range(length))

        try:
            oracle_proc = subprocess.run(
                [oracle_path, fuzz_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{fuzz_input}' with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{fuzz_input}'")

        try:
            agent_proc = subprocess.run(
                [agent_path, fuzz_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{fuzz_input}' with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input '{fuzz_input}'")

        assert agent_output == oracle_output, (
            f"Mismatch on input '{fuzz_input}'.\n"
            f"Expected (Oracle): {oracle_output!r}\n"
            f"Got (Agent): {agent_output!r}"
        )