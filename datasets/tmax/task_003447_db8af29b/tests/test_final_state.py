# test_final_state.py

import os
import subprocess
import json
import random
import pytest

def get_entity_ids():
    env = os.environ.copy()
    env["PGPASSWORD"] = "audit123"
    cmd = [
        "psql",
        "-h", "localhost",
        "-p", "5432",
        "-U", "audit",
        "-d", "compliance",
        "-t",
        "-c", "SELECT id FROM entities;"
    ]
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query PostgreSQL for entity IDs: {e.stderr}")

    ids = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    return ids

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/audit_oracle"
    agent_path = "/app/audit_checker.py"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}"

    all_ids = get_entity_ids()
    assert len(all_ids) > 0, "No entity IDs found in the database."

    random.seed(42)
    fuzz_inputs = random.sample(all_ids, min(50, len(all_ids)))

    for entity_id in fuzz_inputs:
        # Run oracle
        oracle_cmd = [oracle_path, "--entity-id", entity_id]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {entity_id}:\n{oracle_res.stderr}"

        # Run agent
        agent_cmd = ["python3", agent_path, "--entity-id", entity_id]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input {entity_id}.\nStderr: {agent_res.stderr}")

        try:
            oracle_json = json.loads(oracle_res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON on input {entity_id}:\n{oracle_res.stdout}")

        try:
            agent_json = json.loads(agent_res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON on input {entity_id}.\nOutput was:\n{agent_res.stdout}")

        if agent_json != oracle_json:
            pytest.fail(
                f"Output mismatch for --entity-id {entity_id}.\n"
                f"Expected (Oracle):\n{json.dumps(oracle_json, indent=2)}\n\n"
                f"Got (Agent):\n{json.dumps(agent_json, indent=2)}"
            )