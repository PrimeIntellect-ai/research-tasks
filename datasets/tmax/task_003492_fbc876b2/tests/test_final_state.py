# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    ops = ['+', '-', '*', '/']
    for _ in range(n):
        parts = ["REQ"]

        # target
        if random.random() < 0.2:
            # invalid target (contains symbols)
            target = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=5))
            # ensure at least one symbol if we intended it to be invalid
            target += random.choice("!@#$%")
        else:
            # valid target
            target = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        parts.append(target)

        # rate limit
        if random.random() < 0.7:
            limit = random.randint(0, 1000)
            parts.append(f"RATE {limit}")

        # expression
        if random.random() < 0.7:
            num1 = random.randint(-100, 100)
            num2 = random.randint(-100, 100)
            op = random.choice(ops)
            parts.append(f"EXPR {num1} {op} {num2}")

        inputs.append(" ".join(parts))
    return inputs

def test_parser_exists_and_executable():
    script_path = "/home/user/parser.sh"
    assert os.path.isfile(script_path), f"Agent script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Agent script at {script_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle_parser"
    agent_path = "/home/user/parser.sh"

    assert os.path.isfile(oracle_path), f"Oracle parser not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle parser at {oracle_path} is not executable"

    inputs = generate_fuzz_inputs(n=1000, seed=1337)

    for i, req_str in enumerate(inputs):
        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, req_str],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_res = subprocess.run(
            [agent_path, req_str],
            capture_output=True,
            text=True
        )
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input {i}:\n"
            f"Input: {req_str}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}\n"
            f"Agent stderr: {agent_res.stderr.strip()}"
        )