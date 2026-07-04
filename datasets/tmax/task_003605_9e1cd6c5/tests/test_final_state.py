# test_final_state.py

import os
import sys
import json
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/new_router.py"
ORACLE_BIN = "/app/legacy_router_oracle"

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BIN), f"Oracle missing at {ORACLE_BIN}"
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle not executable at {ORACLE_BIN}"

    random.seed(42)

    char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/?=&+._-"
    prefixes = ["/api/", "/graphql", "/secure", "/public", "/admin", ""]

    # Generate random fuzzing inputs
    fuzz_inputs = []
    for _ in range(5000):
        prefix = random.choice(prefixes)
        length = random.randint(5, 100)
        suffix_length = max(0, length - len(prefix))
        suffix = "".join(random.choice(char_set) for _ in range(suffix_length))
        fuzz_inputs.append(prefix + suffix)

    # Inject edge cases explicitly to ensure they are covered
    edge_cases = [
        "/secure?token=3",
        "/secure/data?token=20",
        "/secure?token=4",
        "/secure?token=abc",
        "/secure?other=1",
        "/api/test.php",
        "/public/index.php?user=1",
        "/graphql?query=test",
        "/api/users?id=5"
    ]

    all_inputs = edge_cases + fuzz_inputs

    for url_input in all_inputs:
        # Run oracle
        oracle_cmd = [ORACLE_BIN, url_input]
        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=2)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {url_input}")

        # Run agent
        agent_cmd = [sys.executable, AGENT_SCRIPT, url_input]
        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=2)
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: {url_input}")

        # Parse JSON to compare structure instead of exact string (handles key order, spacing)
        try:
            oracle_json = json.loads(oracle_output)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON on input: {url_input}\nOutput: {oracle_output}")

        try:
            agent_json = json.loads(agent_output)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON on input: {url_input}\nOutput: {agent_output}")

        assert agent_json == oracle_json, (
            f"Mismatch on input: {url_input}\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output:  {agent_json}"
        )