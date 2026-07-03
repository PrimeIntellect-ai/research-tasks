# test_final_state.py

import os
import sqlite3
import subprocess
import random
import pytest
import json

def test_fast_lineage_fuzz_equivalence():
    db_path = "/home/user/data_lineage.db"
    agent_script = "/home/user/fast_lineage.py"
    oracle_binary = "/app/legacy_lineage"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.exists(oracle_binary), f"Oracle binary missing at {oracle_binary}"
    assert os.path.exists(db_path), f"Database missing at {db_path}"

    # Fetch all dataset IDs
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM datasets;")
    all_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(all_ids) > 0, "No datasets found in the database."

    # Generate 50 random inputs
    random.seed(42)
    sample_size = min(50, len(all_ids))
    fuzz_inputs = random.sample(all_ids, sample_size)

    for dataset_id in fuzz_inputs:
        # Run oracle
        oracle_cmd = [oracle_binary, db_path, str(dataset_id)]
        oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_result.returncode == 0, f"Oracle failed on input {dataset_id}:\n{oracle_result.stderr}"
        oracle_output = oracle_result.stdout.strip()

        # Run agent
        agent_cmd = ["python3", agent_script, db_path, str(dataset_id)]
        agent_result = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_result.returncode == 0, f"Agent script failed on input {dataset_id}:\n{agent_result.stderr}"
        agent_output = agent_result.stdout.strip()

        # Try to parse both as JSON to allow for formatting differences, or compare exactly
        try:
            oracle_json = json.loads(oracle_output)
            agent_json = json.loads(agent_output)
            assert oracle_json == agent_json, (
                f"Output mismatch for dataset {dataset_id}.\n"
                f"Oracle JSON:\n{json.dumps(oracle_json, indent=2)}\n"
                f"Agent JSON:\n{json.dumps(agent_json, indent=2)}"
            )
        except json.JSONDecodeError:
            # Fallback to exact string match if not valid JSON
            assert oracle_output == agent_output, (
                f"Output mismatch for dataset {dataset_id}.\n"
                f"Oracle Output:\n{oracle_output}\n"
                f"Agent Output:\n{agent_output}"
            )