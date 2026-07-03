# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        depth = random.randint(1, 50)
        has_anomaly = random.choice([True, False])

        s = "{"
        if has_anomaly:
            s += f'"anomaly_score": {random.uniform(0, 100):.2f}, "cpu_temp": {random.randint(50, 150)}, '

        s += '"nested": '
        for _ in range(depth):
            s += "["
        s += "42"
        for _ in range(depth):
            s += "]"

        target_len = random.randint(50, 10000)
        padding_len = target_len - len(s) - 1
        if padding_len > 0:
            # Add padding to meet the length requirement
            padding = "".join(random.choices(string.ascii_letters, k=padding_len))
            s += f', "pad": "{padding}"'

        s += "}"

        # Mildly malformed 10% of the time
        if random.random() < 0.1:
            s = s[:-1]

        inputs.append(s.encode('utf-8'))
    return inputs

def test_executable_exists():
    agent_path = "/home/user/fixed_processor"
    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_processor"
    agent_path = "/home/user/fixed_processor"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"

    inputs = generate_fuzz_inputs(1000)

    for i, inp in enumerate(inputs):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path], 
                input=inp, 
                capture_output=True, 
                timeout=1
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            # If oracle times out, skip this input
            continue

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path], 
                input=inp, 
                capture_output=True, 
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent executable timed out on input {i}:\n{inp[:200]}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on input {i}.\n"
                f"Input (truncated): {inp[:200]}\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}"
            )

def test_valgrind_memory_leaks():
    agent_path = "/home/user/fixed_processor"
    if not os.path.isfile(agent_path):
        pytest.skip("Agent executable not found")

    # Test memory leaks on a few inputs
    inputs = generate_fuzz_inputs(10)

    for i, inp in enumerate(inputs):
        cmd = [
            "valgrind",
            "--leak-check=full",
            "--error-exitcode=1",
            "--errors-for-leak-kinds=definite,indirect",
            agent_path
        ]
        try:
            proc = subprocess.run(
                cmd,
                input=inp,
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 1:
                pytest.fail(
                    f"Valgrind detected memory leaks on input {i}.\n"
                    f"Input (truncated): {inp[:200]}\n"
                    f"Valgrind stderr:\n{proc.stderr.decode('utf-8', errors='replace')}"
                )
        except FileNotFoundError:
            pytest.skip("Valgrind not installed, skipping memory leak check.")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Valgrind timed out on input {i}")