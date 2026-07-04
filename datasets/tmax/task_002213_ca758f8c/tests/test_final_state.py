# test_final_state.py

import os
import sys
import sqlite3
import random
import string
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/plan_restore.py"
ORACLE_SCRIPT = "/opt/verifier/oracle_plan_restore.py"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_db(db_path, num_tables):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE tables (
            id INTEGER PRIMARY KEY,
            table_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE foreign_keys (
            id INTEGER PRIMARY KEY,
            child_table_id INTEGER,
            parent_table_id INTEGER
        )
    """)

    # Generate random table names
    table_names = set()
    while len(table_names) < num_tables:
        table_names.add(generate_random_string(random.randint(5, 15)))
    table_names = list(table_names)

    # Insert tables
    for i, name in enumerate(table_names):
        cursor.execute("INSERT INTO tables (id, table_name) VALUES (?, ?)", (i + 1, name))

    # Generate random DAG edges
    # To ensure it's a DAG, we only allow edges from i to j where i < j
    max_edges = (num_tables * (num_tables - 1)) // 4
    num_edges = random.randint(0, max_edges)

    possible_edges = [(i, j) for i in range(num_tables) for j in range(i + 1, num_tables)]
    random.shuffle(possible_edges)

    edges = possible_edges[:num_edges]

    for e in edges:
        parent_id = e[0] + 1
        child_id = e[1] + 1
        cursor.execute("INSERT INTO foreign_keys (parent_table_id, child_table_id) VALUES (?, ?)", (parent_id, child_id))

    conn.commit()
    conn.close()

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(200):
            db_path = os.path.join(tmpdir, f"test_{i}.db")
            num_tables = random.randint(5, 50)
            create_random_db(db_path, num_tables)

            # Run oracle
            oracle_proc = subprocess.run(
                [sys.executable, ORACLE_SCRIPT, db_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on DB {i}:\n{oracle_proc.stderr}"
            oracle_output = oracle_proc.stdout.strip()

            # Run agent
            agent_proc = subprocess.run(
                [sys.executable, AGENT_SCRIPT, db_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert agent_proc.returncode == 0, f"Agent script failed on DB {i}:\n{agent_proc.stderr}"
            agent_output = agent_proc.stdout.strip()

            assert agent_output == oracle_output, (
                f"Output mismatch on DB {i} with {num_tables} tables.\n"
                f"Oracle: {oracle_output}\n"
                f"Agent : {agent_output}"
            )