# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = '/verifier/oracle.py'
    agent_path = '/home/user/process.py'

    assert os.path.isfile(oracle_path), f"Oracle script not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script not found at {agent_path}"

    random.seed(42)

    # Generate 100 random inputs
    inputs = []

    # Add some edge cases explicitly
    # 1. Empty array
    inputs.append([])

    # 2. All unknown
    inputs.append([{"x": 1.0, "y": 2.0, "category": "unknown"}, {"x": 3.0, "y": 4.0, "category": "unknown"}])

    # 3. Only 1 valid
    inputs.append([{"x": 1.0, "y": 2.0, "category": "A"}, {"x": 3.0, "y": 4.0, "category": "unknown"}])

    # 4. Perfectly collinear
    inputs.append([{"x": 1.0, "y": 2.0, "category": "A"}, {"x": 2.0, "y": 4.0, "category": "B"}, {"x": 3.0, "y": 6.0, "category": "A"}])

    # 5. Zero variance in x
    inputs.append([{"x": 1.0, "y": 2.0, "category": "A"}, {"x": 1.0, "y": 4.0, "category": "B"}, {"x": 1.0, "y": 6.0, "category": "A"}])

    # 6. Zero variance in y
    inputs.append([{"x": 1.0, "y": 2.0, "category": "A"}, {"x": 2.0, "y": 2.0, "category": "B"}, {"x": 3.0, "y": 2.0, "category": "A"}])

    # Fill the rest with random data
    while len(inputs) < 100:
        length = random.randint(0, 50)
        arr = []
        for _ in range(length):
            arr.append({
                "x": random.uniform(-100, 100),
                "y": random.uniform(-100, 100),
                "category": random.choice(["A", "B", "unknown"])
            })
        inputs.append(arr)

    for i, inp in enumerate(inputs):
        inp_str = json.dumps(inp)

        # Run oracle
        oracle_proc = subprocess.run(
            ['python3', oracle_path],
            input=inp_str,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ['python3', agent_path],
            input=inp_str,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input {i}: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input {i}.\n"
            f"Input: {inp_str}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )