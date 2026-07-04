# test_final_state.py

import os
import random
import subprocess
import pytest
import sqlite3

def test_fuzz_equivalence():
    oracle = "/app/oracle_cleaner"
    agent = "/home/user/cleaner/target/release/cleaner"

    assert os.path.exists(agent), f"Agent binary not found at {agent}"
    assert os.access(agent, os.X_OK), f"Agent binary is not executable"

    random.seed(42)
    lines = []
    for _ in range(10000):
        dev_id = "DEV-" + "".join(random.choices("ABCDEF0123456789", k=4)) if random.random() < 0.5 else "".join(random.choices("ABCDEF0123456789", k=8))
        temp = random.uniform(-50.0, 150.0)

        notes = "notes"
        for _ in range(3):
            if random.random() < 0.5:
                notes += f"\\u{random.randint(0, 0xFFFF):04x}"
            else:
                notes += f"\\u{random.choice(['g', 'h', 'i', 'j'])}{random.randint(0, 0xfff):03x}"

        lines.append(f'{{"device_id":"{dev_id}","temperature":{temp},"notes":"{notes}"}}')

    input_data = "\n".join(lines) + "\n"

    proc_oracle = subprocess.run([oracle], input=input_data.encode('utf-8'), capture_output=True)
    proc_agent = subprocess.run([agent], input=input_data.encode('utf-8'), capture_output=True)

    assert proc_oracle.returncode == 0, "Oracle failed on fuzz input"
    assert proc_agent.returncode == 0, f"Agent failed on fuzz input with stderr: {proc_agent.stderr.decode(errors='ignore')}"

    if proc_oracle.stdout != proc_agent.stdout:
        oracle_lines = proc_oracle.stdout.decode('utf-8', errors='replace').splitlines()
        agent_lines = proc_agent.stdout.decode('utf-8', errors='replace').splitlines()

        for i, (ol, al) in enumerate(zip(oracle_lines, agent_lines)):
            if ol != al:
                pytest.fail(f"Mismatch at output line {i}.\nExpected: {ol}\nGot: {al}")

        pytest.fail(f"Output lengths differ. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}")

def test_pipeline_and_db():
    assert os.path.exists("/home/user/pipeline.sh"), "pipeline.sh missing at /home/user/pipeline.sh"
    assert os.path.exists("/home/user/clean_data.db"), "clean_data.db missing at /home/user/clean_data.db"

    conn = sqlite3.connect("/home/user/clean_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings'")
    assert cursor.fetchone() is not None, "Table 'readings' not found in clean_data.db"

    cursor.execute("SELECT COUNT(*) FROM readings")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'readings' is empty, pipeline did not insert data properly."
    conn.close()