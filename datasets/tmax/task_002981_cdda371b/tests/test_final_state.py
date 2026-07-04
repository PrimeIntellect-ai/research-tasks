# test_final_state.py
import subprocess
import random
import string
import os
import pytest

def rand_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_secure_auth_accuracy():
    script_path = "/home/user/secure_auth.py"
    binary_path = "/app/legacy_auth"

    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"

    matches = 0
    total = 50

    random.seed(42)  # For reproducibility

    for _ in range(total):
        user = rand_string(random.randint(4, 12))
        pwd = rand_string(random.randint(8, 20))

        try:
            expected = subprocess.check_output([binary_path, user, pwd], text=True, stderr=subprocess.STDOUT).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Legacy binary failed. Output: {e.output}")

        try:
            actual = subprocess.check_output(['python3', script_path, user, pwd], text=True, stderr=subprocess.STDOUT).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Python script failed. Output: {e.output}")

        if expected == actual:
            matches += 1
        else:
            pytest.fail(f"Mismatch for user='{user}', pwd='{pwd}'. Expected: '{expected}', Actual: '{actual}'")

    accuracy = matches / total
    assert accuracy >= 1.0, f"Accuracy: {accuracy}. Expected >= 1.0"