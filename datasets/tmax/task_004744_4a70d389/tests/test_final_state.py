# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/opt/oracle_processor"
AGENT_PATH = "/home/user/api_processor/build/processor"

def generate_v1_json():
    user_ident = random.randint(-10000, 100000)
    year = random.randint(2000, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    registration_timestamp = f"{year}-{month:02d}-{day:02d}T10:00:00Z"

    payload_data = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + "=="
    status_code = random.choice([-1, 0, 1, 2, 404, 200])

    extra_field = ''.join(random.choices(string.ascii_lowercase, k=5))
    extra_val = random.random()

    obj = {
        "user_ident": user_ident,
        "registration_timestamp": registration_timestamp,
        "payload_data": payload_data,
        "status_code": status_code,
        extra_field: extra_val
    }

    return json.dumps(obj)

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}. Did you compile the project successfully?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"

    random.seed(42)
    num_tests = 1000

    for i in range(num_tests):
        input_json = generate_v1_json()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_json,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input: {input_json}\nError: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {input_json}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_json,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: {input_json}")

        assert agent_proc.returncode == 0, f"Agent exited with code {agent_proc.returncode} on input: {input_json}\nStderr: {agent_proc.stderr}"

        assert "\n" not in agent_output, f"Agent output is not on a single line for input: {input_json}"

        try:
            oracle_json = json.loads(oracle_output)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON: {oracle_output}")

        try:
            agent_json = json.loads(agent_output)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON: '{agent_output}'\nInput was: {input_json}")

        assert agent_json == oracle_json, f"Mismatch on input: {input_json}\nExpected: {oracle_json}\nGot: {agent_json}"