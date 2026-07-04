# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_EXECUTABLE = "/home/user/mc_estimator"
ORACLE_EXECUTABLE = "/app/oracle_mc_estimator"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_EXECUTABLE), f"Agent executable not found at {AGENT_EXECUTABLE}"
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable {AGENT_EXECUTABLE} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_EXECUTABLE), f"Oracle executable not found at {ORACLE_EXECUTABLE}"
    assert os.access(ORACLE_EXECUTABLE, os.X_OK), f"Oracle executable {ORACLE_EXECUTABLE} is not executable"

    random.seed(42)
    num_iterations = 100

    for i in range(num_iterations):
        # Generate random number of floats N in [10, 500]
        N = random.randint(10, 500)
        # Generate N floats uniformly distributed between 0.0 and 40.0
        floats = [random.uniform(0.0, 40.0) for _ in range(N)]
        input_str = " ".join(f"{f:.6f}" for f in floats)
        input_bytes = (input_str + "\n").encode('utf-8')

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_EXECUTABLE],
                input=input_bytes,
                capture_output=True,
                timeout=5,
                check=True
            )
            oracle_output = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i+1}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i+1} with error: {e.stderr.decode('utf-8')}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_EXECUTABLE],
                input=input_bytes,
                capture_output=True,
                timeout=5,
                check=True
            )
            agent_output = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on iteration {i+1}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on iteration {i+1} with error: {e.stderr.decode('utf-8')}")

        # Compare outputs
        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i+1} (N={N}).\n"
            f"Input (first 100 chars): {input_str[:100]}...\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output: {agent_output}"
        )