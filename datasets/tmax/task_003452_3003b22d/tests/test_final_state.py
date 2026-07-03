# test_final_state.py

import json
import random
import hashlib
import subprocess
import os
import pytest
from urllib.parse import quote

def generate_fuzz_inputs():
    random.seed(42)
    inputs = []
    salt = "winter storm"
    hosts = ["example.com", "test.org", "app.local"]

    for i in range(1000):
        host = random.choice(hosts)

        category = i % 4

        if category == 0:
            # invalid signature
            next_val = "/dashboard"
            path = f"/login?next={quote(next_val)}"
            cookie = "auth_sig=badhash123456"
        elif category == 1:
            # malicious payload
            malicious = random.choice(["JaVaScripT:alert(1)", "data:text/html,...", "../etc/passwd"])
            path = f"/login?next={quote(malicious)}"
            expected_hash = hashlib.sha256(f"{host}{path}{salt}".encode()).hexdigest()
            cookie = f"auth_sig={expected_hash}"
        elif category == 2:
            # open redirect
            redirect = random.choice(["https://evil.com/login", "//attacker.com/steal"])
            path = f"/login?next={quote(redirect)}"
            expected_hash = hashlib.sha256(f"{host}{path}{salt}".encode()).hexdigest()
            cookie = f"auth_sig={expected_hash}"
        else:
            # valid
            valid = random.choice(["/dashboard", f"https://{host}/home"])
            path = f"/login?next={quote(valid)}"
            expected_hash = hashlib.sha256(f"{host}{path}{salt}".encode()).hexdigest()
            cookie = f"auth_sig={expected_hash}"

        data = {
            "host": host,
            "path": path,
            "cookie": cookie
        }
        inputs.append(json.dumps(data))

    return inputs

def test_policy_fuzz_equivalence():
    """Fuzz the agent's policy.py against the oracle script to ensure identical behavior."""
    agent_path = "/home/user/policy.py"
    oracle_path = "/verify/oracle.py"

    assert os.path.exists(agent_path), f"Agent script missing: {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle script missing: {oracle_path}"

    inputs = generate_fuzz_inputs()

    for inp in inputs:
        oracle_proc = subprocess.run(["python3", oracle_path], input=inp.encode(), capture_output=True)
        agent_proc = subprocess.run(["python3", agent_path], input=inp.encode(), capture_output=True)

        oracle_out = oracle_proc.stdout.decode().strip()
        agent_out = agent_proc.stdout.decode().strip()

        assert oracle_out == agent_out, (
            f"Mismatch detected!\n"
            f"Input JSON: {inp}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Actual (Agent): {agent_out}"
        )