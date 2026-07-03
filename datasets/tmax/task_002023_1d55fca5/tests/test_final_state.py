# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def generate_fuzz_inputs(n=5000):
    random.seed(42)
    sensors = ["temp", "pressure", "humidity", "vibration", "flow"]
    statuses = ["ok", "warn", "error", "unknown"]

    inputs = []
    for _ in range(n):
        obj = {
            "id": random.randint(0, 100000),
            "sensor": random.choice(sensors),
            "sensor_reading": f"{random.randint(0, 100)}.{random.randint(10**14, 10**24 - 1)}"
        }

        rand_val = random.random()
        if rand_val < 0.10:
            # metadata missing completely
            pass
        elif rand_val < 0.20:
            # metadata exists but status missing
            obj["metadata"] = {"other_key": "value"}
        else:
            # normal
            obj["metadata"] = {"status": random.choice(statuses), "other_key": "value"}

        inputs.append(json.dumps(obj))

    return "\n".join(inputs) + "\n"

def test_fixed_processor_exists():
    assert os.path.isfile('/app/fixed_processor.py'), "/app/fixed_processor.py is missing. You must create it."

def test_fuzz_equivalence():
    oracle_path = '/app/oracle_processor'
    agent_path = '/app/fixed_processor.py'

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} is missing!"
    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing!"

    inputs_str = generate_fuzz_inputs(5000)
    input_bytes = inputs_str.encode('utf-8')

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_path],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15
    )
    oracle_output = oracle_proc.stdout.decode('utf-8').strip().split('\n')

    # Run agent
    agent_proc = subprocess.run(
        ['python3', agent_path],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15
    )
    agent_output = agent_proc.stdout.decode('utf-8').strip().split('\n')

    input_lines = inputs_str.strip().split('\n')

    assert len(agent_output) == len(oracle_output), (
        f"Output line count mismatch. Oracle produced {len(oracle_output)} lines, "
        f"but fixed_processor.py produced {len(agent_output)} lines."
    )

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_output, agent_output)):
        if oracle_line != agent_line:
            pytest.fail(
                f"Mismatch at line {i+1}!\n"
                f"Input JSON:\n{input_lines[i]}\n\n"
                f"Expected Output (Oracle):\n{oracle_line}\n\n"
                f"Actual Output (fixed_processor.py):\n{agent_line}"
            )