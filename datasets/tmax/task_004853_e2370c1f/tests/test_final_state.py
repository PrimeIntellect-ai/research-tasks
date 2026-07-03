# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fixed_decoder_exists_and_executable():
    path = "/home/user/fixed_decoder.sh"
    assert os.path.isfile(path), f"Missing fixed decoder script at {path}"
    assert os.access(path, os.X_OK), f"Fixed decoder at {path} is not executable"

def generate_random_input(force_zero=False):
    num_blocks = random.randint(1, 5)
    hex_chars = "0123456789ABCDEF"
    result = ""
    for i in range(num_blocks):
        if force_zero and i == 0:
            count_hex = "00"
        else:
            count_hex = random.choice(hex_chars) + random.choice(hex_chars)
        char_hex = random.choice("4567") + random.choice(hex_chars)
        result += count_hex + char_hex
    return result

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_decoder"
    agent_path = "/home/user/fixed_decoder.sh"

    assert os.path.isfile(oracle_path), f"Oracle decoder missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent decoder missing at {agent_path}"

    random.seed(42)
    iterations = 50

    for i in range(iterations):
        # Force a '00' count every 5 iterations to test the boundary condition explicitly
        force_zero = (i % 5 == 0)
        test_input = generate_random_input(force_zero=force_zero)

        try:
            oracle_proc = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input}")

        try:
            agent_proc = subprocess.run(
                [agent_path, test_input],
                capture_output=True,
                text=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out (possible infinite loop) on input: {test_input}")

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on input {test_input}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert agent_output == oracle_output, \
            f"Output mismatch on input {test_input}.\nExpected (Oracle): {repr(oracle_output)}\nGot (Agent): {repr(agent_output)}"