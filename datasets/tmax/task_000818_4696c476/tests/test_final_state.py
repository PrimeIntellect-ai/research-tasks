# test_final_state.py

import os
import glob
import subprocess
import csv
import tempfile
import pytest
from datetime import datetime, timedelta

CLEANER_SCRIPT = "/home/user/cleaner.py"
EVIL_DIR = "/home/user/data/evil/"
CLEAN_DIR = "/home/user/data/clean/"
LOG_FILE = "/home/user/processing.log"

def test_cleaner_script_exists():
    assert os.path.exists(CLEANER_SCRIPT), f"Cleaner script missing at {CLEANER_SCRIPT}"
    assert os.path.isfile(CLEANER_SCRIPT), f"{CLEANER_SCRIPT} is not a file"

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert len(evil_files) > 0, "No evil files found to test."

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for evil_file in evil_files:
            out_file = os.path.join(tmpdir, "out.csv")
            result = subprocess.run(
                ["python3", CLEANER_SCRIPT, evil_file, out_file],
                capture_output=True
            )
            if result.returncode != 1:
                bypassed_files.append(os.path.basename(evil_file))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def parse_datetime(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        # Fallback for common formats if fromisoformat fails
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

def process_clean_logic(input_csv):
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return [], 0

    parsed_rows = []
    for r in rows:
        parsed_rows.append({
            'timestamp': parse_datetime(r['timestamp']),
            'sensor_alpha': float(r['sensor_alpha']) if r['sensor_alpha'] else None,
            'sensor_beta': float(r['sensor_beta']) if r['sensor_beta'] else None,
            'sensor_gamma': float(r['sensor_gamma']) if r['sensor_gamma'] else None,
        })

    parsed_rows.sort(key=lambda x: x['timestamp'])
    start_time = parsed_rows[0]['timestamp']
    end_time = parsed_rows[-1]['timestamp']

    # Create 5-minute intervals
    intervals = []
    curr = start_time
    while curr <= end_time:
        intervals.append(curr)
        curr += timedelta(minutes=5)

    sensors = ['sensor_alpha', 'sensor_beta', 'sensor_gamma']
    expected_data = []

    for sensor in sensors:
        # Extract sensor data
        sensor_data = {r['timestamp']: r[sensor] for r in parsed_rows if r[sensor] is not None}

        last_val = None
        ffill_count = 0

        for t in intervals:
            val = None
            if t in sensor_data:
                val = sensor_data[t]
                last_val = val
                ffill_count = 0
            else:
                if last_val is not None and ffill_count < 3:
                    val = last_val
                    ffill_count += 1
                else:
                    val = 0.0
                    last_val = None # Reset after 3 ffills

            expected_data.append({
                'timestamp': t.strftime("%Y-%m-%d %H:%M:%S"),
                'sensor_name': sensor,
                'value': val
            })

    return expected_data, len(rows)

def test_clean_corpus_processed():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert len(clean_files) > 0, "No clean files found to test."

    failed_files = []

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    with tempfile.TemporaryDirectory() as tmpdir:
        for clean_file in clean_files:
            out_file = os.path.join(tmpdir, "out.csv")
            result = subprocess.run(
                ["python3", CLEANER_SCRIPT, clean_file, out_file],
                capture_output=True
            )

            if result.returncode != 0:
                failed_files.append((os.path.basename(clean_file), "Non-zero exit code"))
                continue

            if not os.path.exists(out_file):
                failed_files.append((os.path.basename(clean_file), "Output file not created"))
                continue

            expected_data, orig_rows = process_clean_logic(clean_file)

            # Read output
            with open(out_file, 'r') as f:
                reader = csv.DictReader(f)
                out_rows = list(reader)

            if len(out_rows) != len(expected_data):
                failed_files.append((os.path.basename(clean_file), f"Row count mismatch: expected {len(expected_data)}, got {len(out_rows)}"))
                continue

            # Basic schema check
            if set(out_rows[0].keys()) != {'timestamp', 'sensor_name', 'value'}:
                failed_files.append((os.path.basename(clean_file), "Invalid output schema"))
                continue

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/failed: {failed_files}"

def test_log_entries():
    assert os.path.exists(LOG_FILE), f"Log file missing at {LOG_FILE}"

    with open(LOG_FILE, 'r') as f:
        log_content = f.read()

    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    for clean_file in clean_files:
        basename = os.path.basename(clean_file)
        assert basename in log_content, f"Log entry for {basename} not found in {LOG_FILE}"
        assert "[SUCCESS] Processed" in log_content, "Log format missing [SUCCESS] tag"