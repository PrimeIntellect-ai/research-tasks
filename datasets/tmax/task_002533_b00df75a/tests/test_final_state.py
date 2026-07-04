# test_final_state.py

import os
import random
import subprocess
import pytest

def test_solution_exists_and_executable():
    solution_path = "/home/user/solution"
    assert os.path.exists(solution_path), f"The solution executable {solution_path} does not exist."
    assert os.path.isfile(solution_path), f"The path {solution_path} is not a file."
    assert os.access(solution_path, os.X_OK), f"The file {solution_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle.bin"
    solution_path = "/home/user/solution"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing."
    assert os.access(oracle_path, os.X_OK), f"Oracle {oracle_path} not executable."
    assert os.path.exists(solution_path), f"Solution {solution_path} missing."

    random.seed(42)
    N = 1000
    input_size = 64

    for i in range(N):
        test_input = bytes(random.choices(range(256), k=input_size))

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                capture_output=True,
                check=True,
                timeout=1
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle crashed on iteration {i} with input {test_input.hex()}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i} with input {test_input.hex()}")

        try:
            solution_proc = subprocess.run(
                [solution_path],
                input=test_input,
                capture_output=True,
                check=True,
                timeout=1
            )
            solution_output = solution_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Solution crashed on iteration {i} with input {test_input.hex()}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Solution timed out on iteration {i} with input {test_input.hex()}")

        assert oracle_output == solution_output, (
            f"Mismatch on iteration {i}.\n"
            f"Input (hex): {test_input.hex()}\n"
            f"Oracle output (hex): {oracle_output.hex()}\n"
            f"Solution output (hex): {solution_output.hex()}"
        )