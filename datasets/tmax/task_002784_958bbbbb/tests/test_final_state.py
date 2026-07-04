# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_input(length):
    chars = string.ascii_letters + string.digits + " \n"
    delimiter = "TERMINATE_TRANSACTION_99X"

    # Generate random string
    res = []
    current_len = 0
    while current_len < length:
        if random.random() < 0.05:  # 5% chance to insert delimiter
            res.append(delimiter)
            current_len += len(delimiter)
        else:
            c = random.choice(chars)
            res.append(c)
            current_len += 1

    return "".join(res)[:length]

def test_optimized_pipeline_exists():
    agent_script = "/home/user/optimized_pipeline.sh"
    assert os.path.exists(agent_script), f"Optimized pipeline script missing at {agent_script}"
    assert os.path.isfile(agent_script), f"{agent_script} is not a file"

def test_fuzz_equivalence():
    oracle_path = "/app/reference_oracle"
    agent_script = "/home/user/optimized_pipeline.sh"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    random.seed(42)
    N = 100

    for i in range(N):
        length = random.randint(50, 5000)
        test_input = generate_random_input(length).encode('utf-8')

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                capture_output=True,
                timeout=5,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {i}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {i} with error: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                ["/bin/bash", agent_script],
                input=test_input,
                capture_output=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {i}. Make sure there are no infinite loops.")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed on input {i} with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

        if oracle_output != agent_output:
            # Try to decode for better error message, fallback to repr
            try:
                oracle_str = oracle_output.decode('utf-8')
                agent_str = agent_output.decode('utf-8')
                input_str = test_input.decode('utf-8')
            except UnicodeDecodeError:
                oracle_str = repr(oracle_output)
                agent_str = repr(agent_output)
                input_str = repr(test_input)

            error_msg = (
                f"Mismatch on fuzz test {i+1}/{N}.\n"
                f"Input length: {length}\n"
                f"--- Input (first 200 chars) ---\n{input_str[:200]}\n"
                f"--- Expected Output (Oracle) ---\n{oracle_str[:500]}\n"
                f"--- Actual Output (Agent) ---\n{agent_str[:500]}\n"
            )
            pytest.fail(error_msg)