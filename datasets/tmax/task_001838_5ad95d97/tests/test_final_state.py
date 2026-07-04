# test_final_state.py

import os
import sqlite3
import subprocess
import random
import tempfile
import pytest
from datetime import datetime, timedelta

AGENT_SCRIPT = "/home/user/chain_builder.py"
ORACLE_BINARY = "/app/legacy_chain_builder"
NUM_TESTS = 20

@pytest.fixture(scope="session")
def test_databases(tmp_path_factory):
    random.seed(42)
    db_dir = tmp_path_factory.mktemp("dbs")
    db_paths = []

    for i in range(NUM_TESTS):
        db_path = db_dir / f"test_{i}.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE backups (
                backup_id INTEGER PRIMARY KEY,
                parent_id INTEGER,
                backup_type TEXT,
                size_bytes INTEGER,
                timestamp DATETIME
            )
        """)

        num_records = random.randint(10, 50)
        start_time = datetime(2023, 1, 1)

        for j in range(1, num_records + 1):
            backup_id = j
            # 20% chance of no parent, otherwise pick a random previous backup as parent
            if j == 1 or random.random() < 0.2:
                parent_id = None
            else:
                parent_id = random.randint(1, j - 1)

            backup_type = random.choice(['FULL', 'DIFF', 'INC'])
            # Ensure at least some FULL backups
            if j <= 3:
                backup_type = 'FULL'

            size_bytes = random.randint(1000, 1000000)
            timestamp = start_time + timedelta(hours=j)

            cursor.execute(
                "INSERT INTO backups (backup_id, parent_id, backup_type, size_bytes, timestamp) VALUES (?, ?, ?, ?, ?)",
                (backup_id, parent_id, backup_type, size_bytes, timestamp.isoformat())
            )

        conn.commit()
        conn.close()
        db_paths.append(str(db_path))

    return db_paths

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence(test_databases):
    assert os.path.isfile(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary is not executable: {ORACLE_BINARY}"

    for db_path in test_databases:
        # Run oracle
        oracle_res = subprocess.run(
            [ORACLE_BINARY, db_path],
            capture_output=True,
            text=True
        )
        assert oracle_res.returncode == 0, f"Oracle failed on {db_path}:\n{oracle_res.stderr}"
        oracle_out = oracle_res.stdout

        # Run agent
        agent_res = subprocess.run(
            ["python3", AGENT_SCRIPT, db_path],
            capture_output=True,
            text=True
        )
        assert agent_res.returncode == 0, f"Agent script failed on {db_path}:\n{agent_res.stderr}"
        agent_out = agent_res.stdout

        # Compare
        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on database: {db_path}\n"
                f"--- Oracle Output ---\n{oracle_out}\n"
                f"--- Agent Output ---\n{agent_out}\n"
            )