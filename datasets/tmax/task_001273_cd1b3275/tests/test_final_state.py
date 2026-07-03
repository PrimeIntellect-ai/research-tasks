# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    num_lines = random.randint(10, 50)
    lines = []
    sensors_list = ["alpha", "beta", "gamma", "delta"]

    for _ in range(num_lines):
        time = random.randint(1000000, 1001000)
        # 10% chance to duplicate a timestamp by picking a previously used one
        if lines and random.random() < 0.1:
            time = json.loads(random.choice(lines))["time"]

        sensors = {}
        num_sensors = random.randint(1, 4)
        chosen_sensors = random.sample(sensors_list, num_sensors)
        for s in chosen_sensors:
            sensors[s] = round(random.uniform(-100.0, 100.0), 4)

        record = {"time": time, "sensors": sensors}
        lines.append(json.dumps(record))

    return "\n".join(lines) + "\n"

def test_final_analysis_csv_exists():
    path = "/home/user/final_analysis.csv"
    assert os.path.isfile(path), f"Missing final output file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"File {path} is empty."

def test_process_telemetry_fuzz_equivalence():
    agent_script = "/home/user/process_telemetry"
    oracle_script = "/app/oracle_processor"

    assert os.path.isfile(agent_script), f"Missing agent script: {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable: {agent_script}"

    assert os.path.isfile(oracle_script), f"Missing oracle script: {oracle_script}"
    assert os.access(oracle_script, os.X_OK), f"Oracle script is not executable: {oracle_script}"

    N = 100
    for i in range(N):
        input_data = generate_fuzz_input(seed=42 + i)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input:\n{input_data}\nStderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input:\n{input_data}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz iteration {i}.\n"
            f"Input JSONL:\n{input_data}\n"
            f"Oracle Output:\n{oracle_out}\n"
            f"Agent Output:\n{agent_out}\n"
        )