# test_final_state.py

import os
import sqlite3
import random
import subprocess
import pytest

def test_database_edges_inserted():
    db_path = "/app/lineage.db"
    assert os.path.exists(db_path), f"Database {db_path} not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    expected_edges = [
        (12, 45, 2),
        (45, 8, 5),
        (8, 31, 1)
    ]

    for src, tgt, wt in expected_edges:
        cursor.execute("SELECT COUNT(*) FROM edges WHERE source=? AND target=? AND weight=?", (src, tgt, wt))
        count = cursor.fetchone()[0]
        assert count >= 1, f"Expected edge (source={src}, target={tgt}, weight={wt}) from the audio transcription was not found in the edges table."

    conn.close()

def test_fuzz_equivalence():
    agent_bin = "/home/user/path_finder"
    oracle_bin = "/app/oracle_path_finder"

    assert os.path.exists(agent_bin), f"Agent binary {agent_bin} not found. Did you compile it?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} not found."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    N = 500

    for _ in range(N):
        u = random.randint(1, 50)
        v = random.randint(1, 50)

        agent_cmd = [agent_bin, str(u), str(v)]
        oracle_cmd = [oracle_bin, str(u), str(v)]

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5)
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired as e:
            pytest.fail(f"Timeout while running binary on input ({u}, {v}). Command: {e.cmd}. You might have an infinite loop.")

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input ({u}, {v}).\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )