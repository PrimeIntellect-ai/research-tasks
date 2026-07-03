# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_path(length):
    components = []
    for _ in range(length):
        choice = random.random()
        if choice < 0.2:
            components.append("..")
        elif choice < 0.3:
            components.append(".")
        elif choice < 0.4:
            components.append("") # will create //
        else:
            name_len = random.randint(1, 10)
            name = "".join(random.choices(string.ascii_letters + string.digits + "_", k=name_len))
            components.append(name)

    path = "/".join(components)
    if random.random() < 0.2:
        path = "/" + path
    if random.random() < 0.2:
        path = path + "/"
    return path

def test_fuzz_equivalence():
    agent_executable = "/home/user/path_resolver"
    oracle_executable = "/app/oracle_path_resolver"

    assert os.path.isfile(agent_executable), f"Agent executable not found at {agent_executable}"
    assert os.access(agent_executable, os.X_OK), f"Agent executable {agent_executable} is not executable"

    assert os.path.isfile(oracle_executable), f"Oracle executable not found at {oracle_executable}"
    assert os.access(oracle_executable, os.X_OK), f"Oracle executable {oracle_executable} is not executable"

    random.seed(42)
    num_tests = 10000

    inputs = []
    for _ in range(num_tests):
        length = random.randint(1, 50)
        inputs.append(generate_random_path(length))

    input_data = "\n".join(inputs) + "\n"

    try:
        agent_process = subprocess.run(
            [agent_executable],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Agent executable timed out on fuzz inputs.")

    try:
        oracle_process = subprocess.run(
            [oracle_executable],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle executable timed out on fuzz inputs.")

    agent_outputs = agent_process.stdout.splitlines()
    oracle_outputs = oracle_process.stdout.splitlines()

    assert len(agent_outputs) == len(oracle_outputs), \
        f"Output line count mismatch: expected {len(oracle_outputs)}, got {len(agent_outputs)}"

    for i, (agent_out, oracle_out) in enumerate(zip(agent_outputs, oracle_outputs)):
        assert agent_out == oracle_out, \
            f"Mismatch on input '{inputs[i]}':\nExpected: {oracle_out}\nGot: {agent_out}"