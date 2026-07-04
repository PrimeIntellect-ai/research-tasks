# test_final_state.py
import os
import json
import random
import subprocess
import pytest

AGENT_PROCESSOR = "/home/user/processor"
ORACLE_PROCESSOR = "/app/oracle_processor"

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    for _ in range(n):
        sensor_id = f"S{random.randint(1, 100)}"
        length = random.randint(5, 20)
        readings = []
        for _ in range(length):
            if random.random() < 0.3:
                readings.append(None)
            else:
                readings.append(round(random.uniform(0.0, 100.0), 2))

        # Ensure at least one non-null value for interpolation to work
        if all(x is None for x in readings):
            readings[random.randint(0, length - 1)] = round(random.uniform(0.0, 100.0), 2)

        inputs.append(json.dumps({"sensor_id": sensor_id, "readings": readings}))
    return "\n".join(inputs) + "\n"

def test_agent_processor_exists():
    assert os.path.isfile(AGENT_PROCESSOR), f"Agent's processor not found at {AGENT_PROCESSOR}"
    assert os.access(AGENT_PROCESSOR, os.X_OK), f"Agent's processor at {AGENT_PROCESSOR} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PROCESSOR), f"Oracle processor not found at {ORACLE_PROCESSOR}"

    # Ensure Redis is populated for the test
    if os.path.isfile("/app/init_redis.py"):
        subprocess.run(["python3", "/app/init_redis.py"], capture_output=True)

    fuzz_data = generate_fuzz_inputs(1000)

    oracle_proc = subprocess.run(
        [ORACLE_PROCESSOR],
        input=fuzz_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle processor failed: {oracle_proc.stderr}"
    oracle_output = oracle_proc.stdout.strip().split('\n')

    agent_proc = subprocess.run(
        [AGENT_PROCESSOR],
        input=fuzz_data,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent processor failed: {agent_proc.stderr}"
    agent_output = agent_proc.stdout.strip().split('\n')

    fuzz_lines = fuzz_data.strip().split('\n')

    assert len(agent_output) == len(oracle_output), f"Output line count mismatch. Expected {len(oracle_output)}, got {len(agent_output)}"

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_output, agent_output)):
        assert oracle_line == agent_line, (
            f"Mismatch at input line {i+1}:\n"
            f"Input:  {fuzz_lines[i]}\n"
            f"Oracle: {oracle_line}\n"
            f"Agent:  {agent_line}"
        )

def test_e2e_sh_success():
    if os.path.isfile("/app/test_e2e.sh"):
        result = subprocess.run(["bash", "/app/test_e2e.sh"], capture_output=True, text=True)
        assert result.returncode == 0, f"End-to-end test script failed:\n{result.stdout}\n{result.stderr}"