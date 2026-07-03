# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_BINARY = "/home/user/project/rle_encoder"
ORACLE_BINARY = "/app/legacy_encoder"
MAIN_CPP = "/home/user/project/main.cpp"

def test_executable_exists():
    assert os.path.exists(AGENT_BINARY), f"Executable {AGENT_BINARY} was not built."
    assert os.path.isfile(AGENT_BINARY), f"Path {AGENT_BINARY} is not a file."
    assert os.access(AGENT_BINARY, os.X_OK), f"Executable {AGENT_BINARY} is not executable."

def test_patch_applied():
    assert os.path.exists(MAIN_CPP), f"File {MAIN_CPP} is missing."
    with open(MAIN_CPP, "r") as f:
        content = f.read()
    assert "<chrono>" in content, "The benchmarking patch does not appear to be applied to main.cpp."

def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_binary(binary_path, arg):
    try:
        result = subprocess.run(
            [binary_path, arg],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {binary_path} timed out on input of length {len(arg)}.")
    except Exception as e:
        pytest.fail(f"Execution of {binary_path} failed: {e}")

def test_fuzz_equivalence():
    random.seed(42)

    # Test empty string explicitly
    test_inputs = [""]

    # Generate 500 random strings
    for _ in range(500):
        length = random.randint(1, 2000)
        test_inputs.append(generate_random_string(length))

    for i, test_input in enumerate(test_inputs):
        oracle_stdout, oracle_code = run_binary(ORACLE_BINARY, test_input)
        agent_stdout, agent_code = run_binary(AGENT_BINARY, test_input)

        assert agent_stdout == oracle_stdout, (
            f"Output mismatch on iteration {i}.\n"
            f"Input length: {len(test_input)}\n"
            f"Input preview: {test_input[:50]}...\n"
            f"Expected (Oracle) output preview: {oracle_stdout[:50]}...\n"
            f"Actual (Agent) output preview: {agent_stdout[:50]}..."
        )