# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_input():
    """Generates a single line of input matching the required regex pattern."""
    id_val = random.randint(0, 9999)
    user_len = random.randint(3, 8)
    user = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=user_len))
    ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    def gen_sensor():
        if random.random() < 0.3:
            return "NA"
        return f"{random.randint(0, 999)}.{random.randint(0, 9)}"

    s1, s2, s3 = gen_sensor(), gen_sensor(), gen_sensor()
    return f"ID:{id_val};USER:{user};IP:{ip};S1:{s1};S2:{s2};S3:{s3}"

def test_fuzz_equivalence():
    """Test that the agent's processor exactly matches the oracle's output on random inputs."""
    random.seed(42)
    num_iterations = 1000
    inputs = [generate_input() for _ in range(num_iterations)]
    input_str = "\n".join(inputs) + "\n"

    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/processor/target/release/processor"

    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}. Did you build in release mode?"

    oracle_proc = subprocess.run([oracle_path], input=input_str, text=True, capture_output=True)
    assert oracle_proc.returncode == 0, f"Oracle failed with error: {oracle_proc.stderr}"

    agent_proc = subprocess.run([agent_path], input=input_str, text=True, capture_output=True)
    assert agent_proc.returncode == 0, f"Agent failed with error: {agent_proc.stderr}"

    oracle_out = oracle_proc.stdout.strip().split("\n")
    agent_out = agent_proc.stdout.strip().split("\n")

    if oracle_out == [""]:
        oracle_out = []
    if agent_out == [""]:
        agent_out = []

    assert len(oracle_out) == len(agent_out), f"Output line count mismatch. Expected {len(oracle_out)}, got {len(agent_out)}"

    for i, (o, a) in enumerate(zip(oracle_out, agent_out)):
        input_idx = i // 3
        assert o == a, (
            f"Mismatch at output line {i+1}.\n"
            f"Input: {inputs[input_idx]}\n"
            f"Expected: {o}\n"
            f"Got:      {a}"
        )

def test_cron_job_setup():
    """Test that the cron job file exists and contains the correct schedule and command."""
    cron_path = "/etc/cron.d/sensor_processor"
    assert os.path.exists(cron_path), f"Cron file {cron_path} is missing."

    with open(cron_path, "r") as f:
        content = f.read()

    expected_pattern = "*/5 * * * * user /home/user/run_pipeline.sh"
    assert expected_pattern in content, (
        f"Cron file {cron_path} does not contain the expected pattern.\n"
        f"Expected to find: '{expected_pattern}'\n"
        f"Actual content:\n{content}"
    )