# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_db_updated():
    db_path = "/app/warehouse.db"
    assert os.path.exists(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT weight FROM edges WHERE source='C' AND target='D';")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Edge C->D not found in the database"
    assert row[0] == 14, f"Expected weight of C->D to be 14, but got {row[0]}"

def test_shortest_path():
    path_file = "/home/user/shortest_path.txt"
    assert os.path.exists(path_file), f"Shortest path file missing at {path_file}"

    with open(path_file, "r") as f:
        content = f.read().strip()

    assert content == "A,B,E,F", f"Expected shortest path to be 'A,B,E,F', but got '{content}'"

def test_query_filter_adversarial_corpus():
    script_path = "/home/user/query_filter.py"
    assert os.path.exists(script_path), f"Query filter script missing at {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.sql')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.sql')]

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    evil_bypassed = []
    for evil_file in evil_files:
        full_path = os.path.join(evil_dir, evil_file)
        result = subprocess.run(["python3", script_path, full_path], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(evil_file)

    clean_rejected = []
    for clean_file in clean_files:
        full_path = os.path.join(clean_dir, clean_file)
        result = subprocess.run(["python3", script_path, full_path], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(clean_file)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))