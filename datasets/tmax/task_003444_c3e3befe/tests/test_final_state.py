# test_final_state.py

import os
import random
import subprocess
import json
import sqlite3
import pytest

def test_graph_db_repaired():
    """Ensure the database integrity check passes after repair."""
    db_path = "/app/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()[0]
        assert result == "ok", f"Database integrity check failed. Expected 'ok', got: {result}"
    finally:
        conn.close()

def test_go_binary_exists():
    """Ensure the Go binary is compiled and exists."""
    bin_path = "/home/user/query_graph"
    assert os.path.isfile(bin_path), f"Go binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Go binary {bin_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz-equivalence test: compare agent binary output with oracle output."""
    oracle_path = "/app/oracle_query_graph"
    agent_path = "/home/user/query_graph"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} is missing."

    random.seed(42)
    N = 50

    for i in range(N):
        limit = random.randint(1, 20)
        offset = random.randint(0, 50)
        min_score = random.randint(-10, 10)

        args = [str(limit), str(offset), str(min_score)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on inputs {args}: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent failed on inputs {args}: {agent_res.stderr}"

        try:
            oracle_json = json.loads(oracle_res.stdout.strip())
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON on inputs {args}: {oracle_res.stdout}")

        try:
            agent_json = json.loads(agent_res.stdout.strip())
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON on inputs {args}: {agent_res.stdout}")

        assert oracle_json == agent_json, (
            f"Output mismatch on iteration {i+1}/{N} with args: limit={limit}, offset={offset}, min_score={min_score}.\n"
            f"Expected (Oracle): {oracle_json}\n"
            f"Got (Agent): {agent_json}"
        )