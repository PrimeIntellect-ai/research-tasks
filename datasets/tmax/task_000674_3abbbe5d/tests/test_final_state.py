# test_final_state.py

import os
import subprocess
import random
import pytest

def test_recovered_db_exists():
    db_path = "/home/user/recovered_backups.db"
    assert os.path.isfile(db_path), f"Recovered database {db_path} is missing."

def test_analyzer_script_exists_and_executable():
    script_path = "/home/user/backup_analyzer.py"
    assert os.path.isfile(script_path), f"Analyzer script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Analyzer script {script_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_analyzer"
    agent_script = "/home/user/backup_analyzer.py"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} is missing."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."

    random.seed(42)

    for _ in range(50):
        t = random.randint(1700000000, 1700000100)

        # Run oracle
        oracle_cmd = [oracle_path, str(t)]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {t}: {oracle_res.stderr}"
        oracle_output = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["/usr/bin/python3", agent_script, str(t)]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {t}: {agent_res.stderr}"
        agent_output = agent_res.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on input T={t}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )