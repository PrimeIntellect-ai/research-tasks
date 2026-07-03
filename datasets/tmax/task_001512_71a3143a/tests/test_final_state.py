# test_final_state.py

import os
import subprocess
import random
import pytest

def test_solution_exists():
    path = "/home/user/solution.sh"
    assert os.path.exists(path), f"Solution script missing at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def generate_random_float32_hex(seed, count=1000):
    random.seed(seed)
    inputs = []
    for _ in range(count):
        # Generate positive normalized float32
        # Sign = 0
        # Exponent = 1 to 254 (0x01 to 0xFE)
        # Mantissa = 0 to 0x7FFFFF
        exp = random.randint(1, 254)
        mantissa = random.randint(0, 0x7FFFFF)
        val = (exp << 23) | mantissa
        inputs.append(f"{val:08X}")
    return inputs

def test_fuzz_equivalence():
    oracle_path = "/app/bin/sensor_oracle"
    agent_path = "/home/user/solution.sh"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"

    inputs = generate_random_float32_hex(42, 1000)
    input_data = "\n".join(inputs) + "\n"

    try:
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to run: {e.stderr}")

    try:
        agent_proc = subprocess.run(
            ["/bin/bash", agent_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        agent_output = agent_proc.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed to run: {e.stderr}")

    assert len(oracle_output) == len(inputs), f"Oracle output length mismatch: expected {len(inputs)}, got {len(oracle_output)}"
    assert len(agent_output) == len(inputs), f"Agent output length mismatch: expected {len(inputs)}, got {len(agent_output)}"

    for i in range(len(inputs)):
        assert oracle_output[i] == agent_output[i], (
            f"Mismatch on input {inputs[i]}:\n"
            f"Oracle output: {oracle_output[i]}\n"
            f"Agent output:  {agent_output[i]}"
        )