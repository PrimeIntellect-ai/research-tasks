# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_lb_gen"
AGENT_PATH = "/home/user/lb_gen"

def generate_random_ipv4():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_input():
    num_elements = random.randint(1, 20)
    elements = []
    for _ in range(num_elements):
        ip = generate_random_ipv4()
        port = random.randint(1, 65535)
        weight = random.randint(1, 100)
        elements.append(f"{ip}:{port}:{weight}")
    return ",".join(elements)

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent program not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    random.seed(42)
    inputs = [generate_random_input() for _ in range(200)]

    for i, inp in enumerate(inputs):
        try:
            oracle_res = subprocess.run([ORACLE_PATH, inp], capture_output=True, text=True, check=True)
            oracle_output = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{inp}'. Stderr: {e.stderr}")

        try:
            agent_res = subprocess.run([AGENT_PATH, inp], capture_output=True, text=True, check=True)
            agent_output = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{inp}'. Stderr: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input {i+1}/200.\n"
            f"Input: {inp}\n\n"
            f"Expected (Oracle):\n{oracle_output}\n\n"
            f"Got (Agent):\n{agent_output}"
        )