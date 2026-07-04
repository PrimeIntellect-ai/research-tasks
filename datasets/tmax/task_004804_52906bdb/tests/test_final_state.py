# test_final_state.py

import os
import random
import subprocess
import pytest

def test_kg_export_exists_and_executable():
    agent_bin = "/home/user/kg-export"
    assert os.path.exists(agent_bin), f"Agent binary missing: {agent_bin}"
    assert os.path.isfile(agent_bin), f"Agent binary is not a file: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

def test_fuzz_equivalence():
    agent_bin = "/home/user/kg-export"
    oracle_bin = "/opt/oracle/kg-export-oracle"
    db_path = "/home/user/dataset.sqlite"

    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"
    assert os.path.exists(db_path), f"Database missing: {db_path}"

    random.seed(42)

    for i in range(50):
        root_paper_id = random.randint(1, 5000)
        max_depth = random.randint(0, 4)

        args = [db_path, str(root_paper_id), str(max_depth)]

        oracle_cmd = [oracle_bin] + args
        agent_cmd = [agent_bin] + args

        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on round {i+1}.\n"
            f"Args: {args}\n"
            f"Oracle exit code: {oracle_proc.returncode}\n"
            f"Agent exit code: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on round {i+1}.\n"
            f"Args: {args}\n"
            f"Oracle stdout: {oracle_proc.stdout}\n"
            f"Agent stdout: {agent_proc.stdout}"
        )