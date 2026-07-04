# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_decode"
AGENT_PATH = "/home/user/decode"
N_TESTS = 200

def generate_random_hex(byte_len):
    return ''.join(random.choices("0123456789abcdef", k=byte_len * 2))

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    random.seed(42)

    for i in range(N_TESTS):
        byte_len = random.randint(8, 512)
        hex_input = generate_random_hex(byte_len)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=hex_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=hex_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz test {i+1}/{N_TESTS}.\n"
                f"Input (hex): {hex_input}\n"
                f"Expected (Oracle) output (hex): {oracle_out.hex()}\n"
                f"Actual (Agent) output (hex): {agent_out.hex()}"
            )