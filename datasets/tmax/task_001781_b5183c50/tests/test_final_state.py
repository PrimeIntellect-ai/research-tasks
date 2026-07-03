# test_final_state.py
import os
import sqlite3
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/query_oracle"
AGENT_PATH = "/home/user/solution"
NUM_TESTS = 30

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_fuzz_db(db_path, seed):
    rng = random.Random(seed)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE sensors (id INTEGER PRIMARY KEY, name TEXT, category TEXT);")
    cursor.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, sensor_id INTEGER, ts INTEGER, metric REAL);")

    num_sensors = rng.randint(5, 15)
    for i in range(1, num_sensors + 1):
        name = generate_random_string(rng.randint(5, 10))
        category = generate_random_string(rng.randint(3, 8))
        cursor.execute("INSERT INTO sensors (id, name, category) VALUES (?, ?, ?)", (i, name, category))

    num_events = rng.randint(50, 200)
    for i in range(1, num_events + 1):
        sensor_id = rng.randint(1, num_sensors)
        ts = rng.randint(1000, 5000)
        metric = round(rng.uniform(10.0, 100.0), 2)
        cursor.execute("INSERT INTO events (id, sensor_id, ts, metric) VALUES (?, ?, ?, ?)", (i, sensor_id, ts, metric))

    conn.commit()
    conn.close()

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent solution binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent solution binary at {AGENT_PATH} is not executable"

    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_TESTS):
            db_path = os.path.join(tmpdir, f"fuzz_{i}.db")
            create_fuzz_db(db_path, seed=42 + i)

            oracle_res = subprocess.run(
                [ORACLE_PATH, db_path],
                capture_output=True,
                text=True,
                check=False
            )

            agent_res = subprocess.run(
                [AGENT_PATH, db_path],
                capture_output=True,
                text=True,
                check=False
            )

            assert oracle_res.returncode == 0, f"Oracle failed on test {i} with error: {oracle_res.stderr}"
            assert agent_res.returncode == 0, f"Agent solution failed on test {i} with error: {agent_res.stderr}"

            if oracle_res.stdout != agent_res.stdout:
                msg = (
                    f"Mismatch on fuzz test {i}!\n"
                    f"Database path (recreated): {db_path}\n"
                    f"Oracle output (first 500 chars):\n{oracle_res.stdout[:500]}\n...\n"
                    f"Agent output (first 500 chars):\n{agent_res.stdout[:500]}\n..."
                )
                pytest.fail(msg)