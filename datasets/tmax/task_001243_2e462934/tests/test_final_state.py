# test_final_state.py

import os
import sqlite3
import subprocess
import glob
import re
import json
import pytest
from datetime import datetime, timedelta

CLEAN_CORPUS_DIR = "/opt/tests/clean_corpus"
EVIL_CORPUS_DIR = "/opt/tests/evil_corpus"
PIPELINE_SCRIPT = "/home/user/pipeline.py"

def is_evil(line: str) -> bool:
    # The Python equivalent of the crash condition from truth
    if r"\u0000" in line:
        return True
    if re.search(r'\\u[dD][89aAbB][0-9a-fA-F]{2}(?!\\u[dD][c-fC-F][0-9a-fA-F]{2})', line):
        return True
    return False

def get_expected_data(input_file: str):
    valid_records = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for raw_line in f:
            if is_evil(raw_line):
                continue
            try:
                record = json.loads(raw_line)
                valid_records.append(record)
            except json.JSONDecodeError:
                continue

    # Basic deduplication and extraction logic to compare counts
    # This is a simplified check to ensure the pipeline is doing something reasonable
    sensor_records = {}
    for r in valid_records:
        sensor_id = r.get("sensor_id", "").upper()
        timestamp = r.get("timestamp")
        # Just keep track of unique (sensor_id, timestamp) pairs to estimate expected row counts
        sensor_records[(sensor_id, timestamp)] = r

    return sensor_records

def test_pipeline_exists():
    assert os.path.exists(PIPELINE_SCRIPT), f"Pipeline script not found at {PIPELINE_SCRIPT}"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.jsonl"))
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []
    for input_file in clean_files:
        output_db = input_file + ".db"
        if os.path.exists(output_db):
            os.remove(output_db)

        result = subprocess.run(
            ["python3", PIPELINE_SCRIPT, input_file, output_db],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or not os.path.exists(output_db):
            failed_files.append(os.path.basename(input_file))
            continue

        # Verify schema
        conn = sqlite3.connect(output_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_sensors'")
        if not cursor.fetchone():
            failed_files.append(os.path.basename(input_file))
        conn.close()

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/failed: {failed_files}"

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.jsonl"))
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []
    for input_file in evil_files:
        output_db = input_file + ".db"
        if os.path.exists(output_db):
            os.remove(output_db)

        result = subprocess.run(
            ["python3", PIPELINE_SCRIPT, input_file, output_db],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or not os.path.exists(output_db):
            failed_files.append(os.path.basename(input_file))
            continue

        # Verify schema
        conn = sqlite3.connect(output_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_sensors'")
        if not cursor.fetchone():
            failed_files.append(os.path.basename(input_file))
            conn.close()
            continue

        # Ensure it actually processed the valid lines
        cursor.execute("SELECT COUNT(*) FROM processed_sensors")
        count = cursor.fetchone()[0]
        if count == 0:
            failed_files.append(os.path.basename(input_file))

        conn.close()

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed/failed: {failed_files}"