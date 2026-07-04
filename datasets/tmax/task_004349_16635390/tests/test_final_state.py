# test_final_state.py

import os
import random
import subprocess
import json
import pytest

def test_apply_indexes():
    """Apply the user's indexes.sql to the database."""
    indexes_path = "/home/user/indexes.sql"
    assert os.path.isfile(indexes_path), f"Missing {indexes_path}"

    env = os.environ.copy()
    env["PGPASSWORD"] = "etl_password"

    result = subprocess.run(
        ["psql", "-h", "localhost", "-p", "5432", "-U", "etl_user", "-d", "etl_db", "-f", indexes_path],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to apply indexes.sql:\n{result.stderr}"

def test_query_py_exists():
    """Check if the user's query.py exists."""
    query_path = "/home/user/query.py"
    assert os.path.isfile(query_path), f"Missing {query_path}"

def test_fuzz_equivalence():
    """Run fuzz-equivalence testing between oracle and user's script."""
    oracle_path = "/app/oracle_query"
    query_path = "/home/user/query.py"

    assert os.path.isfile(oracle_path), f"Missing oracle binary: {oracle_path}"
    assert os.path.isfile(query_path), f"Missing user script: {query_path}"

    random.seed(42)
    test_ids = [random.randint(1, 1000) for _ in range(100)]

    for user_id in test_ids:
        user_id_str = str(user_id)

        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, user_id_str],
            capture_output=True,
            text=True,
            timeout=5.0
        )
        assert oracle_res.returncode == 0, f"Oracle failed for user_id {user_id}:\n{oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent script
        try:
            agent_res = subprocess.run(
                ["python3", query_path, user_id_str],
                capture_output=True,
                text=True,
                timeout=0.5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out (>0.5s) for user_id {user_id}")

        assert agent_res.returncode == 0, f"Agent script failed for user_id {user_id}:\n{agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        # Parse JSON to ensure exact equivalence in values (ignoring formatting differences)
        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output invalid JSON for user_id {user_id}: {oracle_out}")

        try:
            agent_json = json.loads(agent_out)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output invalid JSON for user_id {user_id}: {agent_out}")

        assert agent_json == oracle_json, (
            f"Mismatch for user_id {user_id}.\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output:  {agent_json}"
        )