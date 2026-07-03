# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_cleaner"
AGENT_PATH = "/home/user/cleaner"

def generate_fuzz_inputs(n=10000, seed=42):
    random.seed(seed)
    inputs = []

    def random_hex():
        return random.choice("0123456789abcdefABCDEF")

    def random_char():
        r = random.random()
        if r < 0.2:
            return f"\\u00{random_hex()}{random_hex()}"
        elif r < 0.4:
            return " "
        elif r < 0.7:
            return random.choice(string.ascii_letters)
        else:
            return random.choice(string.printable)

    for _ in range(n):
        length = random.randint(0, 1024)
        # Generate random string
        s = "".join(random_char() for _ in range(length))

        # Remove newlines to ensure single line input
        s = s.replace('\n', ' ').replace('\r', ' ')

        is_valid = random.random() < 0.3
        if is_valid:
            if len(s) >= 2:
                s = '"' + s[1:-1] + '"'
            elif len(s) == 1:
                s = '""'
            else:
                s = '""'
        else:
            if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
                s = s[1:] + ' '

        inputs.append(s)
    return inputs

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"

    inputs = generate_fuzz_inputs(n=10000)

    for i, test_input in enumerate(inputs):
        input_bytes = (test_input + "\n").encode('utf-8')

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_bytes,
                capture_output=True,
                timeout=2,
                check=False
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {i}: {repr(test_input)}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_bytes,
                capture_output=True,
                timeout=2,
                check=False
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input {i}: {repr(test_input)}")

        assert oracle_out == agent_out, (
            f"Mismatch on input {i}:\n"
            f"Input: {repr(test_input)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )