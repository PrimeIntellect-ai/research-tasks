# test_final_state.py

import os
import subprocess
import tempfile
import csv
import glob
import pytest

SCRIPT_PATH = "/home/user/filter_pipeline.py"
CLEAN_CORPUS_DIR = "/app/data/clean"
EVIL_CORPUS_DIR = "/app/data/evil"

def count_csv_rows(filepath):
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        # return data rows count (excluding header)
        return len(rows) - 1 if len(rows) > 0 else 0

def get_csv_rows(filepath):
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus_preserved():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_CORPUS_DIR}"

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filepath in clean_files:
            basename = os.path.basename(filepath)
            outpath = os.path.join(tmpdir, basename)

            cmd = ["python3", SCRIPT_PATH, "--input", filepath, "--output", outpath]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                failed_files.append((basename, "Script crashed or returned non-zero"))
                continue

            if not os.path.isfile(outpath):
                failed_files.append((basename, "Output file not created"))
                continue

            input_rows = get_csv_rows(filepath)
            output_rows = get_csv_rows(outpath)

            if input_rows != output_rows:
                failed_files.append((basename, f"Expected {len(input_rows)} rows, got {len(output_rows)} rows, or contents differed"))

    if failed_files:
        errors = [f"{name}: {reason}" for name, reason in failed_files]
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/failed.\nDetails:\n" + "\n".join(errors))

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_CORPUS_DIR}"

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filepath in evil_files:
            basename = os.path.basename(filepath)
            outpath = os.path.join(tmpdir, basename)

            cmd = ["python3", SCRIPT_PATH, "--input", filepath, "--output", outpath]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                failed_files.append((basename, "Script crashed or returned non-zero"))
                continue

            if not os.path.isfile(outpath):
                failed_files.append((basename, "Output file not created"))
                continue

            input_rows = get_csv_rows(filepath)
            output_rows = get_csv_rows(outpath)

            # Output should only contain the header
            if len(output_rows) > 1:
                failed_files.append((basename, f"Expected 0 data rows, got {len(output_rows) - 1} rows bypassed"))
            elif len(output_rows) == 1 and len(input_rows) > 0 and output_rows[0] != input_rows[0]:
                failed_files.append((basename, "Header mismatch in output"))

    if failed_files:
        errors = [f"{name}: {reason}" for name, reason in failed_files]
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/failed.\nDetails:\n" + "\n".join(errors))