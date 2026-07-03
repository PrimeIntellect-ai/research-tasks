# test_final_state.py

import os
import sqlite3
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    db_path = "/app/data/graph_backup.db"
    assert os.path.isfile(db_path), f"Database not found at {db_path}"

    agent_script = "/home/user/graph_query.py"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable"

    oracle_script = "/app/oracle/graph_query_oracle.py"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    # Extract all node IDs from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT source FROM edges UNION SELECT DISTINCT target FROM edges")
    nodes = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(nodes) > 0, "No nodes found in the SQLite database"

    # Generate 50 random inputs using a fixed seed
    random.seed(42)
    fuzz_inputs = random.choices(nodes, k=50)

    for node in fuzz_inputs:
        oracle_cmd = [oracle_script, node]
        agent_cmd = [agent_script, node]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle script failed on input '{node}':\n{oracle_res.stderr}"

        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input '{node}':\n{agent_res.stderr}"

        oracle_output = oracle_res.stdout.strip()
        agent_output = agent_res.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on input '{node}'.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )