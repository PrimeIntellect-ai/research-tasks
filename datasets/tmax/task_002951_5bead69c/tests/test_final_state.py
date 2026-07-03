# test_final_state.py

import os
import subprocess
import random
import string
import pytest

AGENT_SCRIPT = "/home/user/generate_flags.py"
ORACLE_BINARY = "/app/oracle_flags"
NUM_TESTS = 500

def generate_fuzz_inputs():
    random.seed(42)
    valid_inputs = ["GLIBC_2.25", "GLIBC_2.28", "GLIBC_2.34"]
    inputs = []

    for _ in range(NUM_TESTS):
        choice = random.random()
        if choice < 0.4:
            # Valid exact input
            inputs.append(random.choice(valid_inputs))
        elif choice < 0.6:
            # Valid input with trailing/leading spaces
            val = random.choice(valid_inputs)
            if random.random() < 0.5:
                val = val + " "
            else:
                val = " " + val
            inputs.append(val)
        elif choice < 0.8:
            # Slight mutation of valid input
            val = random.choice(valid_inputs)
            mutated = list(val)
            mutated[random.randint(0, len(mutated)-1)] = random.choice(string.ascii_letters + string.digits)
            inputs.append("".join(mutated))
        else:
            # Completely random string
            length = random.randint(1, 20)
            val = "".join(random.choices(string.ascii_letters + string.digits + "_-.", k=length))
            inputs.append(val)

    return inputs

def test_generate_flags_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary {ORACLE_BINARY} is not executable"

    inputs = generate_fuzz_inputs()

    # We can run all inputs in a single batch to speed up the test
    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_BINARY],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed with error: {oracle_proc.stderr}"
    oracle_output = oracle_proc.stdout.splitlines()

    # Run agent
    agent_proc = subprocess.run(
        ["python3", AGENT_SCRIPT],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"
    agent_output = agent_proc.stdout.splitlines()

    assert len(oracle_output) == len(inputs), f"Oracle output length ({len(oracle_output)}) does not match input length ({len(inputs)})"
    assert len(agent_output) == len(inputs), f"Agent output length ({len(agent_output)}) does not match input length ({len(inputs)})"

    for i, (inp, oracle_line, agent_line) in enumerate(zip(inputs, oracle_output, agent_output)):
        assert oracle_line == agent_line, (
            f"Mismatch on input {i}: {repr(inp)}\n"
            f"Expected (Oracle): {repr(oracle_line)}\n"
            f"Got (Agent):       {repr(agent_line)}"
        )