# test_final_state.py
import os
import json
import sqlite3
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
EXECUTABLE = "/home/user/cleaner"
AUDIO_FILE = "/app/data/run_id.wav"
EXPECTED_RUN_ID = 8024

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found. Did you compile the Go program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".jsonl")]
    assert evil_files, "No evil corpus files found."

    bypassed = []

    for i, filename in enumerate(evil_files):
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        db_path = f"/tmp/evil_test_{i}.db"

        if os.path.exists(db_path):
            os.remove(db_path)

        with open(filepath, "rb") as f:
            proc = subprocess.run(
                [EXECUTABLE, "--audio", AUDIO_FILE, "--db", db_path],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        if not os.path.exists(db_path):
            continue

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM clean_logs")
            count = cursor.fetchone()[0]
            if count > 0:
                bypassed.append(filename)
        except sqlite3.OperationalError:
            # Table might not be created if no rows inserted, which is fine
            pass
        finally:
            conn.close()

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}"

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".jsonl")]
    assert clean_files, "No clean corpus files found."

    modified = []

    for i, filename in enumerate(clean_files):
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        db_path = f"/tmp/clean_test_{i}.db"

        if os.path.exists(db_path):
            os.remove(db_path)

        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        with open(filepath, "rb") as f:
            proc = subprocess.run(
                [EXECUTABLE, "--audio", AUDIO_FILE, "--db", db_path],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        if not os.path.exists(db_path):
            modified.append(filename)
            continue

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM clean_logs ORDER BY timestamp ASC, id ASC")
            rows = cursor.fetchall()

            if len(rows) != len(lines):
                modified.append(filename)
                continue

            # verify run_id and rolling average
            confidences = []
            valid = True
            for j, row in enumerate(rows):
                if row["run_id"] != EXPECTED_RUN_ID:
                    valid = False
                    break

                record = json.loads(lines[j])
                confidences.append(record["confidence"])

                window = confidences[-5:]
                expected_avg = sum(window) / len(window)

                if abs(row["rolling_avg_conf"] - expected_avg) > 1e-4:
                    valid = False
                    break

            if not valid:
                modified.append(filename)

        except sqlite3.OperationalError:
            modified.append(filename)
        finally:
            conn.close()

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified or missing rows. Offending files: {', '.join(modified)}"