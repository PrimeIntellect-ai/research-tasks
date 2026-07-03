# test_final_state.py

import os
import subprocess
import string
import random
import pytest

def test_processor_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/processor/processor"

    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable at {agent_path} is not executable"

    random.seed(42)
    # Fuzz-input distribution: Random ASCII strings (printable characters), length 1-1000, N=100.
    printable_chars = string.printable

    for _ in range(100):
        length = random.randint(1, 1000)
        input_str = "".join(random.choice(printable_chars) for _ in range(length))
        input_data = input_str.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Output mismatch on input: {input_data!r}\n"
                f"Oracle output: {oracle_proc.stdout!r}\n"
                f"Agent output: {agent_proc.stdout!r}"
            )

def test_api_tests_pass():
    test_dir = "/home/user/api_tests/"
    assert os.path.isdir(test_dir), f"Test directory {test_dir} does not exist"

    result = subprocess.run(["pytest", test_dir], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"API tests did not pass. The correct patch might not have been applied.\n"
        f"Pytest output:\n{result.stdout}\n{result.stderr}"
    )