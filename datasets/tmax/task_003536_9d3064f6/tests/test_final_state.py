# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/log_hasher"
AGENT_PATH = "/home/user/log_parser.py"
NUM_TESTS = 5000
MAX_LEN = 500

def generate_random_string(length):
    chars = string.ascii_letters + string.digits + string.punctuation + " \t"
    return "".join(random.choice(chars) for _ in range(length))

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent program not found at {AGENT_PATH}"

    random.seed(42)
    inputs = []
    for _ in range(NUM_TESTS):
        length = random.randint(0, MAX_LEN)
        inputs.append(generate_random_string(length))

    # Add some specific edge cases
    inputs.append("")
    inputs.append("A" * MAX_LEN)
    inputs.append(" " * 50)

    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )
    assert oracle_proc.returncode == 0, f"Oracle program failed: {oracle_proc.stderr}"
    oracle_outputs = oracle_proc.stdout.strip("\n").split("\n")

    # Run agent
    agent_proc = subprocess.run(
        ["python3", AGENT_PATH],
        input=input_data,
        text=True,
        capture_output=True,
        check=False
    )
    assert agent_proc.returncode == 0, f"Agent program failed: {agent_proc.stderr}"
    agent_outputs = agent_proc.stdout.strip("\n").split("\n")

    assert len(oracle_outputs) == len(inputs), "Oracle output line count mismatch"
    assert len(agent_outputs) == len(inputs), "Agent output line count mismatch"

    for i, (oracle_out, agent_out) in enumerate(zip(oracle_outputs, agent_outputs)):
        if oracle_out != agent_out:
            failed_input = inputs[i]
            pytest.fail(
                f"Mismatch found!\n"
                f"Input (length {len(failed_input)}): {repr(failed_input)}\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent):       {agent_out}"
            )