# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_get_lineage_fuzz_equivalence():
    agent_script = "/home/user/get_lineage.py"
    oracle_script = "/verify/oracle_get_lineage.py"
    data_file = "/home/user/backups.json"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"
    assert os.path.isfile(data_file), f"Data file missing: {data_file}"

    # Load backup IDs
    with open(data_file, "r") as f:
        backups = json.load(f)

    # Assuming backups is a list of dicts or dict of dicts, extract IDs.
    # If it's a list, we get 'id' from each. If dict, we get keys.
    if isinstance(backups, list):
        backup_ids = [b['id'] for b in backups]
    elif isinstance(backups, dict):
        backup_ids = list(backups.keys())
    else:
        pytest.fail("Unexpected format for backups.json")

    assert len(backup_ids) > 0, "No backups found in backups.json"

    # Generate fuzz inputs
    random.seed(42)
    fuzz_inputs = random.sample(backup_ids, min(100, len(backup_ids)))

    for backup_id in fuzz_inputs:
        # Run oracle
        oracle_cmd = ["python3", oracle_script, str(backup_id)]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {backup_id}:\n{oracle_res.stderr}"
        oracle_output = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", agent_script, str(backup_id)]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input {backup_id}.\nStderr: {agent_res.stderr}\nStdout: {agent_res.stdout}")

        agent_output = agent_res.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on input '{backup_id}'.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Actual (Agent)  : {agent_output}"
        )

def test_bug_fixed_in_store():
    store_path = "/app/graph_backup_store/store.py"
    assert os.path.isfile(store_path), f"File {store_path} is missing."

    with open(store_path, "r") as f:
        content = f.read()

    # The original bug was `node.get('parent_id', node['id'])`
    # Ensure it's no longer present.
    assert "node.get('parent_id', node['id'])" not in content and "node.get(\"parent_id\", node[\"id\"])" not in content, \
        "The infinite loop bug in /app/graph_backup_store/store.py was not fixed."