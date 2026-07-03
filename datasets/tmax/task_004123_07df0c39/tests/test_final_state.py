# test_final_state.py

import os
import json
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_auditor"
AGENT_DIR = "/home/user/compliance_auditor"
AGENT_BIN = os.path.join(AGENT_DIR, "target/release/compliance_auditor")

def test_build_agent_code():
    assert os.path.isdir(AGENT_DIR), f"Agent directory {AGENT_DIR} does not exist. Did you initialize the Cargo project?"
    try:
        subprocess.run(
            ["cargo", "build", "--release"],
            cwd=AGENT_DIR,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile agent code in release mode:\n{e.stderr}")
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN} after successful build."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"

    random.seed(42)
    N = 10000

    # Generate all inputs first
    inputs = [
        (random.randint(1, 500), random.randint(1000, 5000))
        for _ in range(N)
    ]

    for user_id, resource_id in inputs:
        args = ["--user", str(user_id), "--resource", str(resource_id)]

        oracle_cmd = [ORACLE_PATH] + args
        agent_cmd = [AGENT_BIN] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {args}. Stderr: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent failed on input {args}. Stderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON on input {args}: {oracle_out}")

        try:
            agent_json = json.loads(agent_out)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON on input {args}: {agent_out}")

        assert agent_json == oracle_json, (
            f"Mismatch on input {args}.\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output:  {agent_json}"
        )