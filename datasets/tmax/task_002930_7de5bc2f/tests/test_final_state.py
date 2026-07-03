# test_final_state.py
import os
import subprocess
import sqlite3
import pytest

def test_query_filter_evil_corpus():
    script_path = "/home/user/query_filter.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    evil_dir = "/verify/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    bypassed = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(filename)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}"

def test_query_filter_clean_corpus():
    script_path = "/home/user/query_filter.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    clean_dir = "/verify/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    modified = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            modified.append(filename)

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified (failed): {modified}"

def test_sql_centrality():
    sql_path = "/home/user/centrality.sql"
    db_path = "/app/backup_graph.db"

    assert os.path.exists(sql_path), f"SQL file not found at {sql_path}"
    assert os.path.exists(db_path), f"Database not found at {db_path}"

    with open(sql_path, "r") as f:
        sql_query = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"SQL execution failed: {e}")
    finally:
        conn.close()

    expected = [
        ('jobA', 2, 1),
        ('jobC', 2, 1),
        ('jobB', 1, 3),
        ('jobD', 1, 3)
    ]

    assert results == expected, f"Expected {expected}, but got {results}"