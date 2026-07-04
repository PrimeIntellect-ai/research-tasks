# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_db_populated():
    """Check that the agent populated the MongoDB collection correctly."""
    try:
        from pymongo import MongoClient
    except ImportError:
        pytest.fail("pymongo is not installed. The agent was supposed to use it.")

    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    try:
        client.admin.command('ping')
    except Exception as e:
        pytest.fail(f"Could not connect to MongoDB: {e}")

    db = client["etl"]
    collection = db["iframes"]
    count = collection.count_documents({})
    assert count > 0, "MongoDB collection 'etl.iframes' is empty. Phase 1 (Data Ingestion) was not completed."

def test_fuzz_equivalence():
    """Fuzz the agent's query script against the oracle script."""
    agent_script = "/home/user/build_query.py"
    oracle_script = "/opt/oracle/query_oracle.py"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)

    for i in range(100):
        min_size = random.randint(1000, 50000)
        max_size = random.randint(min_size, 200000)
        limit = random.randint(1, 200)
        sort_order = random.choice([1, -1])

        input_data = {
            "min_size": min_size,
            "max_size": max_size,
            "limit": limit,
            "sort_order": sort_order
        }
        input_str = json.dumps(input_data)

        agent_res = subprocess.run(
            ["python3", agent_script, input_str],
            capture_output=True,
            text=True
        )
        oracle_res = subprocess.run(
            ["python3", oracle_script, input_str],
            capture_output=True,
            text=True
        )

        assert oracle_res.returncode == 0, f"Oracle script failed on input {input_str}. Error: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent script failed on input {input_str}. Error: {agent_res.stderr}"

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz iteration {i+1}.\n"
            f"Input: {input_str}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )