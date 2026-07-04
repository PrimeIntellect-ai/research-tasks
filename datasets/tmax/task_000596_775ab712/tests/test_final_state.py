# test_final_state.py

import os
import subprocess
import json
import random
import string
import pytest

def test_schema_recovered():
    schema_path = "/home/user/schema.json"
    assert os.path.exists(schema_path), f"Recovered schema file {schema_path} does not exist"

    with open(schema_path, 'r') as f:
        try:
            schema_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Recovered schema file {schema_path} is not valid JSON")

    assert schema_data.get("schema_version") == "v1.4.2", "Schema version is incorrect"
    assert schema_data.get("strict_mode") is False, "Schema strict_mode is incorrect"

def test_agent_script_exists():
    script_path = "/home/user/parse_logs.py"
    assert os.path.exists(script_path), f"Agent script {script_path} does not exist"

def generate_random_log():
    timestamp = f"2023-10-25T12:{random.randint(10, 59)}:{random.randint(10, 59)}Z"
    levels = ["INFO", "WARN", "ERROR", "DEBUG", "FATAL", "INVALID"]
    level = random.choice(levels)
    message_len = random.randint(5, 50)
    message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=message_len))

    # Introduce some malformed logs (missing level, missing spaces, etc.)
    rand_val = random.random()
    if rand_val < 0.05:
        return f"[{timestamp}] {message}" # Missing level
    elif rand_val < 0.1:
        return f"[{timestamp}][{level}]{message}" # Missing spaces

    return f"[{timestamp}] [{level}] {message}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_script = "/home/user/parse_logs.py"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing"
    assert os.access(oracle_path, os.X_OK), f"Oracle {oracle_path} not executable"

    random.seed(42)
    num_tests = 1000

    for _ in range(num_tests):
        log_input = generate_random_log()

        # Run oracle
        try:
            oracle_out = subprocess.check_output([oracle_path, log_input], stderr=subprocess.STDOUT, text=True).strip()
        except subprocess.CalledProcessError as e:
            oracle_out = e.output.strip()

        # Run agent
        try:
            agent_out = subprocess.check_output(["python3", agent_script, log_input], stderr=subprocess.STDOUT, text=True).strip()
        except subprocess.CalledProcessError as e:
            agent_out = e.output.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input: {log_input!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )