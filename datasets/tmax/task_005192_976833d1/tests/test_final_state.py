# test_final_state.py

import os
import random
import string
import subprocess
import hashlib
import pytest

def generate_random_string(length):
    return ''.join(random.choice(string.printable) for _ in range(length))

def generate_valid_input(secret="47"):
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
    level = str(random.randint(0, 100))
    data = f"{username}{level}{secret}"
    token = hashlib.md5(data.encode()).hexdigest()
    return f"USER:{username};ESCALATION:{level};TOKEN:{token}"

def generate_invalid_token_input():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
    level = str(random.randint(0, 100))
    token = ''.join(random.choices(string.hexdigits.lower(), k=32))
    return f"USER:{username};ESCALATION:{level};TOKEN:{token}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_audit_verifier"
    agent_path = "/home/user/audit_verifier/target/release/audit_verifier"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable"

    random.seed(42)

    inputs = []
    # 4000 random strings
    for _ in range(4000):
        length = random.randint(0, 128)
        inputs.append(generate_random_string(length))

    # 500 valid formats with wrong hashes
    for _ in range(500):
        inputs.append(generate_invalid_token_input())

    # 500 correct structures
    for _ in range(500):
        inputs.append(generate_valid_input())

    random.shuffle(inputs)

    for i, inp in enumerate(inputs):
        oracle_proc = subprocess.run([oracle_path, inp], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, inp], capture_output=True, text=True)

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on input {repr(inp)}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        assert agent_proc.stdout == oracle_proc.stdout, \
            f"Stdout mismatch on input {repr(inp)}. Oracle: {repr(oracle_proc.stdout)}, Agent: {repr(agent_proc.stdout)}"