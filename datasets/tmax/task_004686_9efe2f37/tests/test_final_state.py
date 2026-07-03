# test_final_state.py
import os
import subprocess
import random
import json
import sqlite3

def test_network_db_exists():
    db_path = "/home/user/network.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."
    assert os.path.isfile(db_path), f"{db_path} is not a file."

    # Check if 'edges' table exists and has correct columns
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges'")
    assert cur.fetchone() is not None, "Table 'edges' does not exist in the database."

    cur.execute("PRAGMA table_info(edges)")
    columns = {row[1] for row in cur.fetchall()}
    assert {"source", "target", "bytes"}.issubset(columns), f"Table 'edges' is missing required columns. Found: {columns}"
    conn.close()

def test_script_is_executable():
    script_path = "/home/user/query_network.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_fuzz_equivalence():
    agent_script = "/home/user/query_network.py"
    oracle_script = "/opt/oracle/oracle_query_network.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} is missing."

    choices = ["Alpha_1", "Beta_2", "Gamma_3", "Delta_2", "Xray_9", "Zulu_0", "Echo_5"]
    random.seed(42)
    inputs = [random.choice(choices) for _ in range(20)]

    for node_id in inputs:
        # Run agent
        agent_cmd = ["/usr/bin/python3", agent_script, node_id]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {node_id}. Error:\n{agent_res.stderr}"

        # Run oracle
        oracle_cmd = ["/usr/bin/python3", oracle_script, node_id]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle script failed on input {node_id}. Error:\n{oracle_res.stderr}"

        # Parse JSON
        try:
            agent_json = json.loads(agent_res.stdout)
        except json.JSONDecodeError:
            assert False, f"Agent output is not valid JSON on input {node_id}. Output:\n{agent_res.stdout}"

        try:
            oracle_json = json.loads(oracle_res.stdout)
        except json.JSONDecodeError:
            assert False, f"Oracle output is not valid JSON on input {node_id}. Output:\n{oracle_res.stdout}"

        assert agent_json == oracle_json, (
            f"Mismatch on input {node_id}.\n"
            f"Expected: {oracle_json}\n"
            f"Got: {agent_json}"
        )