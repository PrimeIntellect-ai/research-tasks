# test_final_state.py

import os
import subprocess
import random
import pytest

def test_replica_fuzz_equivalence():
    oracle_path = "/app/suspicious_bin"
    replica_path = "/home/user/replica.py"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.access(oracle_path, os.X_OK), f"Oracle binary {oracle_path} is not executable."
    assert os.path.exists(replica_path), f"Replica script {replica_path} is missing."

    random.seed(42)
    # Generate 10000 random 32-bit positive integers
    test_inputs = [str(random.randint(1, 2147483647)) for _ in range(10000)]

    # Add some edge cases
    test_inputs.extend(["0", "1", "86400", "31536000", "2147483647"])

    for val in test_inputs:
        # Run oracle
        try:
            oracle_result = subprocess.run(
                [oracle_path, val],
                capture_output=True,
                text=True,
                timeout=1,
                check=True
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {val}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {val} with error: {e.stderr}")

        # Run replica
        try:
            replica_result = subprocess.run(
                ["python3", replica_path, val],
                capture_output=True,
                text=True,
                timeout=1,
                check=True
            )
            replica_output = replica_result.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Replica script timed out on input {val}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Replica script failed on input {val} with error: {e.stderr}")

        assert oracle_output == replica_output, (
            f"Mismatch on input {val}. "
            f"Oracle output: {oracle_output}, Replica output: {replica_output}"
        )