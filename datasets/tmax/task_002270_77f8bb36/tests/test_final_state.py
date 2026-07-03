# test_final_state.py

import os
import socket
import sqlite3
import subprocess
import random
import pytest

def test_database_indexes_fixed():
    db_path = "/app/data/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = [row[0] for row in cursor.fetchall()]

    assert "bad_idx" not in indexes, "The corrupted index 'bad_idx' was not dropped."

    # Check if there's an index on (source, target)
    cursor.execute("PRAGMA index_list('edges');")
    index_list = cursor.fetchall()

    found_correct_index = False
    for idx in index_list:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = [row[2] for row in cursor.fetchall()]
        if columns == ['source', 'target'] or columns == ['target', 'source']:
            found_correct_index = True
            break

    assert found_correct_index, "A proper index on (source, target) was not created for the 'edges' table."
    conn.close()

def test_etl_script_exists():
    script_path = "/app/etl/compute_metrics.sh"
    assert os.path.isfile(script_path), f"ETL script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"ETL script {script_path} is not executable."

def query_agent(node_id: int) -> str:
    # Query the agent's TCP server on port 8080
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", 8080))
        s.sendall(f"{node_id}\n".encode("utf-8"))
        response = s.recv(1024).decode("utf-8")
        s.close()
        return response
    except Exception as e:
        pytest.fail(f"Failed to query agent server on port 8080 for node {node_id}: {e}")

def query_oracle(node_id: int) -> str:
    # Query the oracle program
    oracle_path = "/verify/reference_oracle.py"
    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} is missing."

    try:
        result = subprocess.run(
            ["python3", oracle_path, str(node_id)],
            capture_output=True,
            text=True,
            timeout=2.0
        )
        if result.returncode != 0:
            # Try passing via stdin if args fail
            result = subprocess.run(
                ["python3", oracle_path],
                input=f"{node_id}\n",
                capture_output=True,
                text=True,
                timeout=2.0
            )
        return result.stdout
    except Exception as e:
        pytest.fail(f"Failed to run oracle program for node {node_id}: {e}")

def test_fuzz_equivalence():
    random.seed(42)
    test_nodes = [random.randint(1, 1000) for _ in range(100)]

    for node_id in test_nodes:
        agent_response = query_agent(node_id)
        oracle_response = query_oracle(node_id)

        # Normalize outputs by stripping whitespace
        agent_clean = agent_response.strip()
        oracle_clean = oracle_response.strip()

        assert agent_clean == oracle_clean, (
            f"Mismatch for node ID {node_id}.\n"
            f"Expected (Oracle): {oracle_clean!r}\n"
            f"Got (Agent): {agent_clean!r}"
        )