# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_executable_exists():
    agent_bin = "/home/user/packet_normalizer"
    assert os.path.isfile(agent_bin), f"Executable {agent_bin} does not exist. Did you compile your Rust program?"
    assert os.access(agent_bin, os.X_OK), f"File {agent_bin} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/packet_normalizer"
    oracle_bin = "/app/oracle_bin"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    for i in range(200):
        length = random.randint(5, 100)
        test_input = "".join(random.choices(charset, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, test_input],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input!r}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin, test_input],
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Your program failed (non-zero exit) on input: {test_input!r}\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Mismatch on input: {test_input!r}\n"
            f"Expected output (from oracle): {oracle_output!r}\n"
            f"Your output: {agent_output!r}"
        )