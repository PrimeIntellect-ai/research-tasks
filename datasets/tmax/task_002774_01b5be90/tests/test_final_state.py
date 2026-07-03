# test_final_state.py

import os
import random
import string
import subprocess
import sqlite3
import pytest

def generate_fuzz_input():
    lines = []
    num_lines = random.randint(10, 50)
    current_ts = random.randint(0, 100)
    for _ in range(num_lines):
        if random.random() < 0.6:
            # valid line
            val = random.uniform(-100.0, 100.0)
            # Add some surrounding noise sometimes
            prefix = ''.join(random.choices(string.ascii_letters, k=random.randint(0, 5)))
            suffix = ''.join(random.choices(string.ascii_letters, k=random.randint(0, 5)))
            lines.append(f"{prefix}[{current_ts}] METRIC_VAL: {val}{suffix}")
            current_ts += random.randint(1, 20)
        else:
            # noise
            noise = ''.join(random.choices(string.ascii_letters + string.digits + " []_:", k=random.randint(5, 30)))
            lines.append(noise)
    return "\n".join(lines)

def test_fuzz_equivalence():
    agent_script = "/home/user/process_feed.py"
    oracle_script = "/app/oracle_process_feed.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} not found."

    random.seed(42)

    for i in range(100):
        fuzz_input = generate_fuzz_input()

        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=fuzz_input,
            text=True,
            capture_output=True
        )

        oracle_proc = subprocess.run(
            ["python3", oracle_script],
            input=fuzz_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {i}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on fuzz input {i}.\n"
                f"Input:\n{fuzz_input}\n\n"
                f"Expected (Oracle):\n{oracle_out}\n\n"
                f"Got (Agent):\n{agent_out}"
            )

def test_pipeline_output():
    db_path = "/home/user/telemetry.db"
    assert os.path.exists(db_path), f"Database {db_path} not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
    assert cursor.fetchone() is not None, "Table 'readings' not found in database."

    # Check rows
    cursor.execute("SELECT timestamp, value FROM readings ORDER BY timestamp ASC;")
    rows = cursor.fetchall()

    assert len(rows) > 0, "No rows found in 'readings' table."

    # Run oracle to get expected output
    # First extract subtitles
    ffmpeg_proc = subprocess.run(
        ["ffmpeg", "-i", "/app/instrument_feed.mp4", "-map", "0:s:0", "-f", "srt", "-"],
        text=True,
        capture_output=True
    )
    assert ffmpeg_proc.returncode == 0, "Failed to extract subtitles from video."

    srt_text = ffmpeg_proc.stdout

    oracle_proc = subprocess.run(
        ["python3", "/app/oracle_process_feed.py"],
        input=srt_text,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, "Oracle failed to process subtitles."

    expected_csv = oracle_proc.stdout.strip().split('\n')
    assert len(expected_csv) > 1, "Oracle produced no data."

    expected_rows = []
    for line in expected_csv[1:]: # skip header
        ts, val = line.split(',')
        expected_rows.append((int(ts), float(val)))

    assert len(rows) == len(expected_rows), f"Row count mismatch. Expected {len(expected_rows)}, got {len(rows)}."

    for (actual_ts, actual_val), (exp_ts, exp_val) in zip(rows, expected_rows):
        assert int(actual_ts) == exp_ts, f"Timestamp mismatch: expected {exp_ts}, got {actual_ts}"
        assert abs(float(actual_val) - exp_val) < 0.01, f"Value mismatch at {exp_ts}: expected {exp_val}, got {actual_val}"

    conn.close()