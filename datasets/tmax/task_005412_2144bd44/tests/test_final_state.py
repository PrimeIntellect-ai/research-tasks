# test_final_state.py
import os
import glob
import subprocess
import csv
import pytest

FILTER_BIN = "/home/user/filter"

def test_filter_binary_exists():
    assert os.path.isfile(FILTER_BIN), f"Executable not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"File at {FILTER_BIN} is not executable"

def test_evil_corpus():
    evil_files = glob.glob("/corpus/evil/*.csv")
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed = []
    for evil_file in evil_files:
        out_file = f"/tmp/out_evil_{os.path.basename(evil_file)}"
        if os.path.exists(out_file):
            os.remove(out_file)

        result = subprocess.run([FILTER_BIN, evil_file, out_file], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(evil_file))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}")

def test_clean_corpus():
    clean_files = glob.glob("/corpus/clean/*.csv")
    assert len(clean_files) > 0, "No clean corpus files found."

    modified = []
    for clean_file in clean_files:
        out_file = f"/tmp/out_clean_{os.path.basename(clean_file)}"
        if os.path.exists(out_file):
            os.remove(out_file)

        result = subprocess.run([FILTER_BIN, clean_file, out_file], capture_output=True)
        if result.returncode != 0:
            modified.append((os.path.basename(clean_file), f"exit code {result.returncode}"))
            continue

        if not os.path.isfile(out_file):
            modified.append((os.path.basename(clean_file), "output file not created"))
            continue

        with open(clean_file, 'r', encoding='utf-8') as f:
            in_rows = list(csv.reader(f))

        with open(out_file, 'r', encoding='utf-8') as f:
            out_rows = list(csv.reader(f))

        if len(in_rows) != len(out_rows):
            modified.append((os.path.basename(clean_file), f"row count mismatch: expected {len(in_rows)}, got {len(out_rows)}"))
            continue

        def sort_key(r):
            try:
                ts = int(r[2])
            except ValueError:
                ts = 0
            return (r[1], -ts)

        try:
            sorted_in_rows = sorted(in_rows, key=sort_key)
            if out_rows != sorted_in_rows:
                modified.append((os.path.basename(clean_file), "sorting incorrect or data modified"))
        except Exception as e:
            modified.append((os.path.basename(clean_file), f"error parsing rows: {e}"))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/failed: {modified}")