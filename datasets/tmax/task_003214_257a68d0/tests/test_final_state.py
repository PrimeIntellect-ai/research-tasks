# test_final_state.py

import os
import sqlite3
import subprocess
import pytest
import glob

def test_database_schema():
    db_path = "/home/user/metadata.db"
    assert os.path.isfile(db_path), f"Database file not found: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audio_logs';")
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'audio_logs' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(audio_logs);")
    columns_info = cursor.fetchall()

    expected_columns = ["id", "filename", "sample_rate", "channels", "bit_depth", "is_safe"]

    actual_columns = [col[1] for col in columns_info]
    actual_types = [col[2].upper() for col in columns_info]

    assert actual_columns == expected_columns, f"Expected columns {expected_columns}, but got {actual_columns}"

    for col_type in actual_types:
        assert col_type == "TEXT", f"Expected all columns to be TEXT, but found {col_type}"

    conn.close()

def test_executable_exists():
    exe_path = "/home/user/wav_validator"
    assert os.path.isfile(exe_path), f"Executable not found: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def test_wav_validator_adversarial_corpus():
    exe_path = "/home/user/wav_validator"
    assert os.path.isfile(exe_path), f"Executable not found: {exe_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    clean_failures = []
    for f in clean_files:
        res = subprocess.run([exe_path, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run([exe_path, f], capture_output=True)
        if res.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    assert not error_msg, " | ".join(error_msg)