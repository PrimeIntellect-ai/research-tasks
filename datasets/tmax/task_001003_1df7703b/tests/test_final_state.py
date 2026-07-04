# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/oracle_process_stream"
AGENT_PATH = "/home/user/process_stream"
NUM_TESTS = 1000

def generate_random_inputs(n):
    random.seed(42)
    inputs = []

    num_invalid = int(n * 0.10)
    num_empty = int(n * 0.05)
    num_valid = n - num_invalid - num_empty

    # Generate empty strings
    for _ in range(num_empty):
        if random.choice([True, False]):
            inputs.append("")
        else:
            inputs.append("\n")

    # Generate invalid strings
    invalid_chars = string.ascii_lowercase + string.digits + "!@#$%^&*()_+-=,<>/?;:\"'[{]}\\|`~"
    for _ in range(num_invalid):
        length = random.randint(1, 100)
        s = "".join(random.choices(string.ascii_uppercase + "." + invalid_chars, k=length))
        # Ensure at least one invalid char
        if not any(c in invalid_chars for c in s):
            s = random.choice(invalid_chars) + s[1:] if length > 0 else random.choice(invalid_chars)
        inputs.append(s)

    # Generate valid strings
    valid_chars = list(string.ascii_uppercase)
    for _ in range(num_valid):
        length = random.randint(1, 100)
        s = []
        for _ in range(length):
            if random.random() < 0.6:
                s.append(".")
            else:
                s.append(random.choice(valid_chars))
        inputs.append("".join(s))

    random.shuffle(inputs)
    return inputs

def run_executable(executable_path, input_str):
    try:
        result = subprocess.run(
            [executable_path],
            input=input_str.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        return result.returncode, result.stdout.decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -2, str(e)

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file is not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file is not executable: {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"

    inputs = generate_random_inputs(NUM_TESTS)

    for i, input_str in enumerate(inputs):
        oracle_code, oracle_out = run_executable(ORACLE_PATH, input_str)
        agent_code, agent_out = run_executable(AGENT_PATH, input_str)

        error_msg = (f"Mismatch on input {i}:\n"
                     f"Input (repr): {repr(input_str)}\n"
                     f"Oracle output: {repr(oracle_out)} (exit code {oracle_code})\n"
                     f"Agent output: {repr(agent_out)} (exit code {agent_code})")

        assert oracle_code == agent_code, error_msg
        assert oracle_out == agent_out, error_msg