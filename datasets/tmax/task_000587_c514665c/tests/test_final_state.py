# test_final_state.py

import os
import glob
import subprocess
import json
import csv
import pytest

def get_sanitizer():
    candidates = glob.glob("/home/user/sanitizer*")
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None

def test_video_telemetry():
    csv_path = "/home/user/video_telemetry.csv"
    assert os.path.isfile(csv_path), f"Missing CSV at {csv_path}"

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert "frame_index" in reader.fieldnames, "Missing frame_index column"
    assert "red_intensity" in reader.fieldnames, "Missing red_intensity column"
    assert len(rows) == 300, f"Expected 300 rows, got {len(rows)}"

    val0 = float(rows[0]["red_intensity"])
    start_val = 0.0 if val0 < 0.5 else 1.0

    for i, row in enumerate(rows):
        block = i // 10
        expected_val = start_val if block % 2 == 0 else (1.0 - start_val)
        val = float(row["red_intensity"])
        assert abs(val - expected_val) < 0.1, f"Frame {i} expected {expected_val}, got {val}"

def test_sanitizer_clean_corpus():
    sanitizer = get_sanitizer()
    assert sanitizer is not None, "Sanitizer script not found or not executable in /home/user/"

    clean_dir = "/app/clean_corpus"
    if not os.path.isdir(clean_dir):
        pytest.skip(f"Clean corpus dir missing: {clean_dir}")

    files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    failed = []
    for f in files:
        path = os.path.join(clean_dir, f)
        with open(path, "rb") as infile:
            original = infile.read()

        proc = subprocess.run([sanitizer], input=original, capture_output=True)
        if proc.returncode != 0 or proc.stdout != original:
            failed.append(f)

    assert not failed, f"{len(failed)} of {len(files)} clean modified: {failed}"

def test_sanitizer_evil_corpus():
    sanitizer = get_sanitizer()
    assert sanitizer is not None, "Sanitizer script not found or not executable in /home/user/"

    evil_dir = "/app/evil_corpus"
    if not os.path.isdir(evil_dir):
        pytest.skip(f"Evil corpus dir missing: {evil_dir}")

    files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed = []
    for f in files:
        path = os.path.join(evil_dir, f)
        with open(path, "rb") as infile:
            evil_data = infile.read()

        proc = subprocess.run([sanitizer], input=evil_data, capture_output=True)
        if proc.returncode != 0:
            failed.append(f"{f} (crashed)")
            continue

        try:
            output = proc.stdout.decode('utf-8').strip()
            if output:
                for line in output.split('\n'):
                    if line.strip():
                        json.loads(line)
        except Exception:
            failed.append(f"{f} (invalid json)")

    assert not failed, f"{len(failed)} of {len(files)} evil bypassed: {failed}"