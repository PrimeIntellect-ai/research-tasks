# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_input(length):
    words = ["START", "END", "ERROR"]
    tokens = []
    for _ in range(length):
        choice = random.random()
        if choice < 0.3:
            tokens.append(random.choice(words))
        else:
            word_len = random.randint(1, 10)
            tokens.append(''.join(random.choices(string.ascii_letters + string.digits, k=word_len)))
    return " ".join(tokens)

def test_fixed_parser_exists():
    assert os.path.isfile("/home/user/fixed_parser.py"), "The file /home/user/fixed_parser.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_cmd = ["python3", "/home/user/fixed_parser.py"]

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"

    random.seed(42)

    for i in range(500):
        length = random.randint(10, 500)
        test_input = generate_random_input(length)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {i}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {i}: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                agent_cmd,
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out (possible infinite loop/memory leak) on input:\n{test_input}")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent crashed on input:\n{test_input}\nStderr:\n{agent_proc.stderr}")

        assert agent_out == oracle_out, (
            f"Mismatch on input {i}:\n"
            f"Input:\n{test_input}\n"
            f"Expected (Oracle):\n{oracle_out}\n"
            f"Got (Agent):\n{agent_out}"
        )