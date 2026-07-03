# test_final_state.py

import os
import json
import random
import string
import datetime
import subprocess
import urllib.request
import time
import pytest

def test_generator_config_fixed():
    config_path = "/home/user/generator_config.env"
    assert os.path.isfile(config_path), f"Expected {config_path} to exist."
    with open(config_path, "r") as f:
        content = f.read()
    assert "REDIS_PORT=6379" in content, "Expected REDIS_PORT=6379 in generator_config.env"

def test_flask_config_fixed():
    config_path = "/home/user/flask_config.env"
    assert os.path.isfile(config_path), f"Expected {config_path} to exist."
    with open(config_path, "r") as f:
        content = f.read()
    assert "REDIS_KEY=incoming_logs" in content, "Expected REDIS_KEY=incoming_logs in flask_config.env"

def test_api_returns_logs():
    # Retry a few times in case the services are still starting up or generating logs
    logs = []
    for _ in range(10):
        try:
            req = urllib.request.Request("http://localhost:5000/logs")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    logs = json.loads(response.read().decode('utf-8'))
                    if isinstance(logs, list) and len(logs) >= 5:
                        break
        except Exception:
            pass
        time.sleep(1)

    assert isinstance(logs, list), "Expected the API to return a JSON array."
    assert len(logs) >= 5, f"Expected at least 5 log entries from the API, but got {len(logs)}."

def test_log_analyzer_executable():
    script_path = "/home/user/log_analyzer.py"
    assert os.path.isfile(script_path), f"Expected {script_path} to exist."
    assert os.access(script_path, os.X_OK), f"Expected {script_path} to be executable."

def test_log_analyzer_fuzz_equivalence():
    # Generate fuzz data
    random.seed(1337)
    levels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

    # Pre-generate some service/message pairs to force duplicates
    pool = []
    for _ in range(50):
        svc = ''.join(random.choices(string.ascii_letters, k=5))
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        pool.append((svc, msg))

    lines = []
    for i in range(1000):
        ts = datetime.datetime(2023, 1, 1, 12, 0, 0, i).isoformat()
        level = random.choice(levels)
        if random.random() < 0.3:
            svc, msg = random.choice(pool)
        else:
            svc = ''.join(random.choices(string.ascii_letters, k=5))
            msg = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        lines.append(f"{ts},{level},{svc},{msg}")

    fuzz_data = "\n".join(lines) + "\n"

    # Run oracle
    oracle_path = "/app/oracle_parser"
    assert os.path.isfile(oracle_path), f"Oracle parser missing at {oracle_path}"

    oracle_proc = subprocess.run(
        [oracle_path], 
        input=fuzz_data, 
        text=True, 
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout

    # Run agent script
    agent_path = "/home/user/log_analyzer.py"
    agent_proc = subprocess.run(
        ["python3", agent_path], 
        input=fuzz_data, 
        text=True, 
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

    agent_output = agent_proc.stdout

    if agent_output != oracle_output:
        # Give a helpful diff for the first mismatch
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()

        for i, (oline, aline) in enumerate(zip(oracle_lines, agent_lines)):
            if oline != aline:
                pytest.fail(f"Mismatch at output line {i+1}:\nOracle: {oline}\nAgent:  {aline}")

        if len(oracle_lines) != len(agent_lines):
            pytest.fail(f"Output line count mismatch: Oracle produced {len(oracle_lines)} lines, Agent produced {len(agent_lines)} lines.")

        pytest.fail("Agent output did not exactly match Oracle output.")