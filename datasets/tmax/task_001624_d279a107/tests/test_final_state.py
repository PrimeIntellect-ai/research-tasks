# test_final_state.py

import os
import random
import subprocess
import pytest

def test_database_exists():
    """Check that the student created the database file."""
    db_path = "/home/user/graph.db"
    assert os.path.exists(db_path), f"Database file is missing: {db_path}"
    assert os.path.isfile(db_path), f"Expected a file at {db_path}"

def test_query_binary_exists():
    """Check that the student created the compiled query binary."""
    query_bin_path = "/home/user/query"
    assert os.path.exists(query_bin_path), f"Compiled binary is missing: {query_bin_path}"
    assert os.path.isfile(query_bin_path), f"Expected a file at {query_bin_path}"
    assert os.access(query_bin_path, os.X_OK), f"Binary is not executable: {query_bin_path}"

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent's binary to ensure exact equivalence."""
    oracle_bin = "/app/oracle_query"
    agent_bin = "/home/user/query"

    assert os.path.exists(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)
    N = 100

    for _ in range(N):
        src = random.randint(0, 255)
        dst = random.randint(0, 255)

        oracle_res = subprocess.run(
            [oracle_bin, str(src), str(dst)],
            capture_output=True,
            text=True
        )

        agent_res = subprocess.run(
            [agent_bin, str(src), str(dst)],
            capture_output=True,
            text=True
        )

        assert agent_res.returncode == oracle_res.returncode, (
            f"Return code mismatch for src={src}, dst={dst}.\n"
            f"Oracle returned: {oracle_res.returncode}\n"
            f"Agent returned: {agent_res.returncode}"
        )

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch for src={src}, dst={dst}.\n"
            f"Oracle output:\n{oracle_res.stdout}\n"
            f"Agent output:\n{agent_res.stdout}"
        )