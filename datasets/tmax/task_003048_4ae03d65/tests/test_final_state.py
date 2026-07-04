# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/policy_engine.bin"
AGENT_SCRIPT = "/home/user/policy_engine.py"
AGENT_CMD = ["/usr/bin/python3", AGENT_SCRIPT]

def generate_random_ip():
    rand_val = random.random()
    if rand_val < 0.2:
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    elif rand_val < 0.4:
        return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    else:
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_port():
    if random.random() < 0.3:
        return 22
    return random.randint(1, 65535)

def generate_random_input():
    ip = generate_random_ip()
    port = generate_random_port()
    key_type = random.choice(["rsa", "dsa", "ecdsa", "ed25519"])
    key_length = random.choice([1024, 2048, 3072, 4096, 256, 521])
    return f"{ip} {port} {key_type} {key_length}"

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)
    num_tests = 1000

    for _ in range(num_tests):
        test_input = generate_random_input()

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{test_input}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{test_input}'")

        # Run agent
        try:
            agent_proc = subprocess.run(
                AGENT_CMD,
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2,
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input '{test_input}'")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script crashed on input '{test_input}'. Stderr: {agent_proc.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input '{test_input}'\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent):       {agent_output}"
        )