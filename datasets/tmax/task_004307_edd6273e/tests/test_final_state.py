# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/metric_oracle"
AGENT_PATH = "/home/user/fast_metric"
NUM_TESTS = 1000

def generate_test_cases(num_tests):
    random.seed(42)
    test_cases = []
    for _ in range(num_tests):
        n = random.randint(3, 15)

        # Array 1
        if random.random() < 0.05:
            val = random.randint(-100, 100)
            arr1 = [val] * n
        else:
            arr1 = [random.randint(-100, 100) for _ in range(n)]

        # Array 2
        if random.random() < 0.05:
            val = random.randint(-100, 100)
            arr2 = [val] * n
        else:
            arr2 = [random.randint(-100, 100) for _ in range(n)]

        str1 = " ".join(map(str, arr1))
        str2 = " ".join(map(str, arr2))
        test_cases.append((str1, str2))

    return test_cases

def run_executable(executable_path, arg1, arg2):
    try:
        result = subprocess.run(
            [executable_path, arg1, arg2],
            capture_output=True,
            text=True,
            check=True,
            timeout=2
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Return code {e.returncode}, stderr: {e.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    test_cases = generate_test_cases(NUM_TESTS)

    for i, (arg1, arg2) in enumerate(test_cases):
        oracle_out = run_executable(ORACLE_PATH, arg1, arg2)
        agent_out = run_executable(AGENT_PATH, arg1, arg2)

        assert oracle_out == agent_out, (
            f"Mismatch on test case {i + 1}/{NUM_TESTS}.\n"
            f"Input 1: '{arg1}'\n"
            f"Input 2: '{arg2}'\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'"
        )