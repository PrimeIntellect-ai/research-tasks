# test_final_state.py
import os
import random
import subprocess
import pytest

def test_regression_script_exists():
    assert os.path.isfile('/home/user/test_regression.py'), "/home/user/test_regression.py is missing."

def test_parse_runner_exists():
    assert os.path.isfile('/home/user/parse_runner.py'), "/home/user/parse_runner.py is missing."

def test_fuzz_equivalence():
    """
    Fuzz the agent's parse_runner.py against the oracle_parser.
    5000 random hex-encoded strings representing byte payloads of length 12 to 128 bytes.
    The first byte is always 0x88.
    """
    random.seed(42)
    oracle_path = '/app/oracle_parser'
    agent_cmd = ['python3', '/home/user/parse_runner.py']

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    for i in range(5000):
        length = random.randint(12, 128)
        payload = bytearray([0x88])
        for _ in range(length - 1):
            payload.append(random.randint(0, 255))

        hex_string = payload.hex()

        oracle_proc = subprocess.run([oracle_path, hex_string], capture_output=True, text=True)
        agent_proc = subprocess.run(agent_cmd + [hex_string], capture_output=True, text=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on input {hex_string} (iteration {i}).\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}\n"
                f"Oracle stderr: {oracle_proc.stderr.strip()}\n"
                f"Agent stderr:  {agent_proc.stderr.strip()}"
            )
            pytest.fail(error_msg)