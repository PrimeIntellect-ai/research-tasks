# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/dataset_encoder"
AGENT_PATH = "/home/user/encoder"

def generate_random_input(length):
    charset = string.ascii_letters + string.digits + " ,"
    return "".join(random.choice(charset) for _ in range(length))

def run_executable(executable_path, input_data):
    result = subprocess.run(
        [executable_path],
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=2
    )
    return result.stdout.decode('utf-8')

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    random.seed(42)

    # Generate 1000 random inputs
    inputs = []
    # Explicitly test empty string and newline only
    inputs.append("")
    inputs.append("\n")
    inputs.append("a,b,c\n")

    for _ in range(997):
        length = random.randint(0, 1024)
        inp = generate_random_input(length)
        # Randomly append newline sometimes
        if random.random() < 0.5:
            inp += "\n"
        inputs.append(inp)

    for i, inp in enumerate(inputs):
        oracle_out = run_executable(ORACLE_PATH, inp)
        try:
            agent_out = run_executable(AGENT_PATH, inp)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent executable timed out on input {i} (length {len(inp)})")
        except Exception as e:
            pytest.fail(f"Agent executable failed on input {i}: {e}")

        if oracle_out != agent_out:
            # Truncate input for display if it's too long
            display_inp = inp if len(inp) <= 100 else inp[:100] + "... (truncated)"
            pytest.fail(
                f"Mismatch on input {i}:\n"
                f"Input: {repr(display_inp)}\n"
                f"Oracle output: {repr(oracle_out)}\n"
                f"Agent output:  {repr(agent_out)}"
            )