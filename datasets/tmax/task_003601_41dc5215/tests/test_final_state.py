# test_final_state.py

import os
import sqlite3
import subprocess
import random
import pytest

DB_PATH = "/home/user/backup_topology.db"
AGENT_SCRIPT = "/home/user/impact_analysis.sh"
ORACLE_SCRIPT = "/app/oracle_impact_analysis.sh"
REPORT_PATH = "/home/user/incident_report.txt"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script not executable: {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), "Oracle script missing"
    assert os.path.isfile(DB_PATH), "Database missing"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT source_node FROM backup_dependencies;")
    nodes = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(nodes) > 0, "No nodes found in the database to fuzz."

    random.seed(42)
    # Generate 50 random inputs
    fuzz_nodes = random.choices(nodes, k=50)

    for node in fuzz_nodes:
        oracle_proc = subprocess.run([ORACLE_SCRIPT, node], capture_output=True, text=True)
        agent_proc = subprocess.run([AGENT_SCRIPT, node], capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"Agent script failed on node {node}:\n{agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch for node '{node}'.\n"
            f"Expected:\n{oracle_out}\n\n"
            f"Got:\n{agent_out}"
        )

def test_incident_report():
    assert os.path.isfile(REPORT_PATH), f"Incident report missing: {REPORT_PATH}"

    target_node = "backup-server-delta"
    oracle_proc = subprocess.run([ORACLE_SCRIPT, target_node], capture_output=True, text=True)
    expected_out = oracle_proc.stdout.strip()

    with open(REPORT_PATH, "r") as f:
        report_out = f.read().strip()

    assert report_out == expected_out, (
        f"Incident report content does not match expected output for node '{target_node}'.\n"
        f"Expected:\n{expected_out}\n\n"
        f"Got:\n{report_out}"
    )