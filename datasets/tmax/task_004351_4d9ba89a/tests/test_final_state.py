# test_final_state.py

import os
import csv
import subprocess
import tempfile
import pytest

BINARY_PATH = "/home/user/filter"
EVIL_CORPUS_DIR = "/opt/verifier/corpora/evil/"
CLEAN_CORPUS_DIR = "/opt/verifier/corpora/clean/"

def run_filter(input_csv, output_csv):
    try:
        result = subprocess.run(
            [BINARY_PATH, input_csv, output_csv],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False

def read_csv(filepath):
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)
    return header, rows

def test_filter_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"File at {BINARY_PATH} is not executable"

def test_evil_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            success = run_filter(input_path, output_path)
            if not success or not os.path.exists(output_path):
                failed_files.append(f"{filename} (execution failed)")
                continue

            header, rows = read_csv(output_path)
            if header != ['id', 'val_A', 'val_B', 'payload']:
                failed_files.append(f"{filename} (bad header)")
            elif len(rows) > 0:
                failed_files.append(f"{filename} ({len(rows)} rows not filtered)")

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: " + ", ".join(failed_files[:5])

def test_clean_corpus():
    if not os.path.isfile(BINARY_PATH):
        pytest.skip("Binary not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
            output_path = os.path.join(tmpdir, filename)

            success = run_filter(input_path, output_path)
            if not success or not os.path.exists(output_path):
                failed_files.append(f"{filename} (execution failed)")
                continue

            orig_header, orig_rows = read_csv(input_path)
            out_header, out_rows = read_csv(output_path)

            if out_header != ['id', 'val_A', 'val_B', 'payload']:
                failed_files.append(f"{filename} (bad header)")
                continue

            if len(orig_rows) != len(out_rows):
                failed_files.append(f"{filename} (row count mismatch: {len(orig_rows)} expected, got {len(out_rows)})")
                continue

            # Expected rows: sort by val_A (stable)
            expected_rows = sorted(orig_rows, key=lambda x: int(x[1]))
            for r in expected_rows:
                r[0] = 'MASKED'

            if out_rows != expected_rows:
                failed_files.append(f"{filename} (content/sort/mask mismatch)")

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/failed: " + ", ".join(failed_files[:5])