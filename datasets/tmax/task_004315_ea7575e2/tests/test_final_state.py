# test_final_state.py

import os
import subprocess
import random
import pytest

def test_processor_exists_and_executable():
    processor_path = "/home/user/processor"
    assert os.path.exists(processor_path), f"Agent binary {processor_path} is missing."
    assert os.path.isfile(processor_path), f"{processor_path} is not a file."
    assert os.access(processor_path, os.X_OK), f"Agent binary {processor_path} is not executable."

def test_anomalies_log_content():
    log_path = "/home/user/anomalies.log"
    assert os.path.exists(log_path), f"Output log {log_path} is missing."

    expected_content = """1700000000,0,100.123
1700000000,2,100.000
1700000000,4,100.999
1700000001,0,12.500
1700000001,1,-5.500
1700000001,3,0.500
"""
    with open(log_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "The content of anomalies.log does not match the expected output."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/processor"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} is missing."

    random.seed(42)
    regex_pool = ["^[0-9]+\\.000$", "^-[0-9]+\\.[1-9]00$", "^42\\.[0-9]{3}$", "^.*$"]

    for i in range(50): # Reduced to 50 for performance in test
        num_lines = random.randint(10, 100)
        lines = []
        for _ in range(num_lines):
            timestamp = random.randint(1600000000, 1700000000)
            regex = random.choice(regex_pool)
            n_floats = random.randint(1, 100)
            floats = [f"{random.uniform(-100, 100):.4f}" for _ in range(n_floats)]
            line = f"{timestamp} {regex} {n_floats} " + " ".join(floats)
            lines.append(line)

        input_data = "\n".join(lines) + "\n"

        try:
            oracle_proc = subprocess.run([oracle_path], input=input_data, text=True, capture_output=True, check=True)
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input:\n{input_data[:200]}...\nError: {e.stderr}")

        try:
            agent_proc = subprocess.run([agent_path], input=input_data, text=True, capture_output=True, check=True)
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on valid input:\n{input_data[:200]}...\nError: {e.stderr}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch found on fuzz test #{i}.\n"
                f"Input (truncated):\n{input_data[:500]}\n\n"
                f"Oracle output (truncated):\n{oracle_output[:500]}\n\n"
                f"Agent output (truncated):\n{agent_output[:500]}"
            )