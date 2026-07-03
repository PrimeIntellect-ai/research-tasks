# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def get_random_string(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(length))

def test_hash_algo_accuracy():
    script_path = "/home/user/hash_algo.py"
    binary_path = "/app/auth_cli"

    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

    matches = 0
    total = 100

    # Use a fixed seed for reproducibility in tests, or random. 
    # The prompt verifier uses random, so we will too, but let's seed it just in case.
    random.seed(42)

    for _ in range(total):
        test_str = get_random_string(random.randint(5, 50))

        # Run binary
        try:
            bin_out = subprocess.check_output([binary_path, test_str]).decode('utf-8').strip()
        except Exception as e:
            pytest.fail(f"Failed to run binary {binary_path} with input {test_str}: {e}")

        # Run Python script
        try:
            py_out = subprocess.check_output(['python3', script_path, test_str]).decode('utf-8').strip()
        except Exception as e:
            py_out = ""

        if bin_out == py_out:
            matches += 1

    accuracy = matches / total
    assert accuracy >= 1.0, f"Accuracy is {accuracy}, expected 1.0. The script output did not match the binary output perfectly."