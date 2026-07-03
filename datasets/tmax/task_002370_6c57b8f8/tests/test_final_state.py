# test_final_state.py

import os
import sys
import json
import random
import string
import sqlite3
import subprocess
import tempfile
import datetime
import pytest

AGENT_SCRIPT = "/home/user/get_latest_backups.py"
ORACLE_SCRIPT = "/opt/oracle/oracle_get_latest.py"
NUM_TESTS = 20

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_db(db_path, seed):
    random.seed(seed)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE clusters (cluster_id INTEGER PRIMARY KEY, cluster_name TEXT);")
    cursor.execute("CREATE TABLE storage_nodes (node_id INTEGER PRIMARY KEY, cluster_id INTEGER, node_name TEXT, region TEXT);")
    cursor.execute("CREATE TABLE backup_logs (log_id INTEGER PRIMARY KEY, node_id INTEGER, database_name TEXT, backup_timestamp DATETIME, backup_size_mb INTEGER, status TEXT);")

    # Generate clusters
    clusters = [(i, f"cluster_{random_string(5)}") for i in range(1, 6)]
    cursor.executemany("INSERT INTO clusters VALUES (?, ?)", clusters)

    # Generate storage_nodes
    num_nodes = random.randint(10, 50)
    regions = ['us-west', 'us-east', 'eu-central', 'ap-south']
    nodes = []
    for i in range(1, num_nodes + 1):
        cluster_id = random.choice(clusters)[0]
        node_name = f"node_{random_string(8)}"
        region = random.choice(regions)
        nodes.append((i, cluster_id, node_name, region))
    cursor.executemany("INSERT INTO storage_nodes VALUES (?, ?, ?, ?)", nodes)

    # Generate backup_logs
    statuses = ['SUCCESS', 'FAILED', 'PENDING']
    logs = []
    log_id = 1

    base_time = datetime.datetime(2023, 1, 1)

    for node in nodes:
        node_id = node[0]
        num_dbs = random.randint(5, 20)
        for _ in range(num_dbs):
            db_name = f"db_{random_string(6)}"
            num_logs = random.randint(10, 100)
            for _ in range(num_logs):
                # Random timestamp within a year
                delta = datetime.timedelta(days=random.randint(0, 365), seconds=random.randint(0, 86400))
                ts = (base_time + delta).isoformat()
                size = random.randint(100, 10000)
                status = random.choice(statuses)
                logs.append((log_id, node_id, db_name, ts, size, status))
                log_id += 1

    cursor.executemany("INSERT INTO backup_logs VALUES (?, ?, ?, ?, ?, ?)", logs)
    conn.commit()
    conn.close()

def run_script(script_path, db_path):
    result = subprocess.run(
        [sys.executable, script_path, db_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        pytest.fail(f"Script {script_path} failed with return code {result.returncode}.\nSTDERR: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Script {script_path} did not output valid JSON.\nSTDOUT: {result.stdout}")

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_TESTS):
            db_path = os.path.join(tmpdir, f"test_{i}.db")
            generate_random_db(db_path, seed=42+i)

            oracle_output = run_script(ORACLE_SCRIPT, db_path)
            agent_output = run_script(AGENT_SCRIPT, db_path)

            if oracle_output != agent_output:
                # Truncate output for error message if too long
                oracle_str = json.dumps(oracle_output, indent=2)
                agent_str = json.dumps(agent_output, indent=2)
                if len(oracle_str) > 1000:
                    oracle_str = oracle_str[:1000] + "\n... (truncated)"
                if len(agent_str) > 1000:
                    agent_str = agent_str[:1000] + "\n... (truncated)"

                pytest.fail(
                    f"Mismatch on generated database {i} (seed {42+i}).\n"
                    f"Oracle output:\n{oracle_str}\n\n"
                    f"Agent output:\n{agent_str}"
                )