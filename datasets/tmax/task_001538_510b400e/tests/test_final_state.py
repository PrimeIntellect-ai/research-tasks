# test_final_state.py

import os
import subprocess
import random
import pytest

def test_config_fixed():
    config_path = "/app/flask_service/config.env"
    assert os.path.isfile(config_path), f"File {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert "REDIS_PORT=6379" in content, "REDIS_PORT is not correctly set to 6379 in config.env"
    assert "PG_PORT=5432" in content, "PG_PORT is not correctly set to 5432 in config.env"
    assert "6380" not in content, "Legacy Redis port 6380 still in config.env"
    assert "5433" not in content, "Legacy Postgres port 5433 still in config.env"

def test_script_exists():
    script_path = "/home/user/workspace/restore_planner.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_fuzz_equivalence():
    script_path = "/home/user/workspace/restore_planner.py"
    oracle_path = "/app/oracle_planner"

    assert os.path.isfile(script_path), "Agent script is missing."
    assert os.path.isfile(oracle_path), "Oracle program is missing."

    random.seed(42)
    test_ids = [str(random.randint(1000, 9999)) for _ in range(50)]

    for db_id in test_ids:
        # Run oracle
        oracle_cmd = [oracle_path, "--db-id", db_id]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on --db-id {db_id}\nStderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_cmd = ["python3", script_path, "--db-id", db_id]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on --db-id {db_id}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on --db-id {db_id}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )