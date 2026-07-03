# test_final_state.py

import os
import subprocess
import pytest
import sqlite3

def test_verify_stream_exists():
    assert os.path.exists("/home/user/verify_stream.py"), "verify_stream.py is missing"

def test_adversarial_corpus():
    script_path = "/home/user/verify_stream.py"
    clean_dir = "/var/opt/corpus/clean"
    evil_dir = "/var/opt/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)] if os.path.exists(clean_dir) else []
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)] if os.path.exists(evil_dir) else []

    clean_failures = []
    for f in clean_files:
        res = subprocess.run(["python3", script_path, "--input", f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run(["python3", script_path, "--input", f], capture_output=True)
        if res.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pipeline_execution_and_db():
    pipeline_script = "/home/user/pipeline.py"
    db_path = "/home/user/metrics.db"

    if os.path.exists(pipeline_script):
        # We run the pipeline script; it should process /var/opt/integration_test/
        # Since the task doesn't specify how the directory is passed, we assume it's hardcoded or uses a default
        # We just run it and check if db is created with the right schema
        subprocess.run(["python3", pipeline_script], capture_output=True)

    assert os.path.exists(db_path), f"Database {db_path} was not created."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rolling_temps';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'rolling_temps' does not exist in the database."

    cursor.execute("PRAGMA table_info(rolling_temps);")
    columns = {row[1] for row in cursor.fetchall()}
    expected_columns = {"sensor_id", "window_end_time", "avg_temperature"}

    assert expected_columns.issubset(columns), f"Table 'rolling_temps' is missing required columns. Found: {columns}"

    conn.close()