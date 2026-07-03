# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_crashing_input_extracted():
    path = "/home/user/crashing_input.txt"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "quarterly report final version.pdf", f"Incorrect content in {path}: {content}"

def test_hasher_executable_exists():
    path = "/home/user/fixed_hasher"
    assert os.path.isfile(path), f"Missing executable at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_hasher_fuzz_equivalence():
    oracle_path = "/app/oracle_hasher"
    agent_path = "/home/user/fixed_hasher"

    assert os.path.isfile(oracle_path), f"Missing oracle at {oracle_path}"
    assert os.path.isfile(agent_path), f"Missing agent executable at {agent_path}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + " "

    for i in range(100):
        length = random.randint(1, 200)
        test_input = "".join(random.choice(charset) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path], input=test_input, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=test_input, text=True, capture_output=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input!r}"
        assert agent_proc.returncode == 0, f"Agent program failed (return code {agent_proc.returncode}) on input: {test_input!r}"
        assert agent_out == oracle_out, f"Mismatch on input {test_input!r}\nExpected (Oracle): {oracle_out}\nGot (Agent): {agent_out}"