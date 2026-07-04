# test_final_state.py

import os
import random
import string
import subprocess
import json
import pytest

def generate_random_log_line():
    year = random.randint(2020, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    timestamp = f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

    level = random.choice(["INFO", "WARN", "ERROR", "FATAL"])

    comp_len = random.randint(3, 10)
    component = "".join(random.choices(string.ascii_lowercase + string.digits + "-", k=comp_len))

    msg_len = random.randint(10, 50)
    message = "".join(random.choices(string.ascii_letters + string.digits + " ", k=msg_len))

    return f"[{timestamp}] {level} - {component}: {message}"

def test_restored_data_exists():
    assert os.path.isdir("/home/user/restored_data"), "Restored data directory is missing. Did the expect script run successfully?"
    assert os.path.isfile("/home/user/restored_data/oracle_parser"), "oracle_parser is missing from restored data."

def test_agent_binary_exists():
    path = "/home/user/uptime_parser"
    assert os.path.isfile(path), f"Agent's binary {path} is missing."
    assert os.access(path, os.X_OK), f"Agent's binary {path} is not executable."

def test_fuzz_equivalence():
    agent_bin = "/home/user/uptime_parser"
    oracle_bin = "/home/user/restored_data/oracle_parser"

    if not os.path.isfile(oracle_bin):
        oracle_bin = "/app/oracle_parser" # Fallback if setup put it here

    assert os.path.isfile(oracle_bin), "Oracle binary not found."
    assert os.path.isfile(agent_bin), "Agent binary not found."

    random.seed(42)

    for _ in range(100):
        log_line = generate_random_log_line()

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_bin],
                input=log_line,
                text=True,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input: {log_line}\nError: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_bin],
                input=log_line,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {log_line}")

        assert agent_proc.returncode == 0, f"Agent binary failed on input: {log_line}\nError: {agent_proc.stderr}"

        assert agent_out == oracle_out, (
            f"Mismatch on input: {log_line}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )