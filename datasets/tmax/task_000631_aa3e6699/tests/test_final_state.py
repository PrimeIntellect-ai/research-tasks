# test_final_state.py

import os
import subprocess
import glob
import csv
import pytest
from io import StringIO

def count_csv_records(file_path_or_content, is_file=True):
    """Counts logical CSV records, properly handling embedded newlines."""
    if is_file:
        with open(file_path_or_content, 'r', newline='', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            return sum(1 for row in reader if row)
    else:
        reader = csv.reader(StringIO(file_path_or_content))
        return sum(1 for row in reader if row)

def test_csv_tracker_executable():
    executable = "/home/user/csv_tracker"
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you compile the C program?"
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_adversarial_corpus_filtering():
    executable = "/home/user/csv_tracker"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    clean_failures = []
    evil_failures = []

    # 1. Test Clean Corpus (MUST preserve/reshape 100%)
    for c_file in clean_files:
        input_records = count_csv_records(c_file, is_file=True)
        expected_output_records = input_records * 2

        with open(c_file, 'rb') as f:
            result = subprocess.run([executable], stdin=f, capture_output=True, text=True, errors='replace')

        if result.returncode != 0:
            clean_failures.append(f"{os.path.basename(c_file)} (process crashed/failed with code {result.returncode})")
            continue

        output_records = count_csv_records(result.stdout, is_file=False)
        if output_records != expected_output_records:
            clean_failures.append(f"{os.path.basename(c_file)} (expected {expected_output_records} records, got {output_records})")

    # 2. Test Evil Corpus (MUST reject 100%)
    for e_file in evil_files:
        with open(e_file, 'rb') as f:
            result = subprocess.run([executable], stdin=f, capture_output=True, text=True, errors='replace')

        output_records = count_csv_records(result.stdout, is_file=False)
        if output_records != 0:
            evil_failures.append(f"{os.path.basename(e_file)} (bypassed {output_records} records)")

    # 3. Surface clear summary on failure
    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failures))
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: " + ", ".join(clean_failures))

    assert not error_messages, " | ".join(error_messages)