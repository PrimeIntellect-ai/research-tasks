# test_final_state.py

import os
import csv
import json
import subprocess
import tempfile
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
SCRIPT_PATH = "/home/user/filter_transcripts.py"
LOG_PATH = "/home/user/experiment_log.jsonl"

def count_csv_rows(filepath):
    if not os.path.exists(filepath):
        return 0
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if not rows:
            return 0
        # Exclude header
        return len(rows) - 1

def run_script(input_csv, output_csv):
    cmd = ["python", SCRIPT_PATH, "--input", input_csv, "--output", output_csv]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean CSV files found to test."

    modified_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in clean_files:
            input_path = os.path.join(CLEAN_DIR, filename)
            output_path = os.path.join(tmpdir, f"out_{filename}")

            input_rows = count_csv_rows(input_path)
            success, stderr = run_script(input_path, output_path)

            if not success:
                modified_files.append(f"{filename} (script crashed: {stderr})")
                continue

            output_rows = count_csv_rows(output_path)
            if output_rows != input_rows:
                modified_files.append(f"{filename} (expected {input_rows} rows, got {output_rows})")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil CSV files found to test."

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for filename in evil_files:
            input_path = os.path.join(EVIL_DIR, filename)
            output_path = os.path.join(tmpdir, f"out_{filename}")

            success, stderr = run_script(input_path, output_path)

            if not success:
                bypassed_files.append(f"{filename} (script crashed: {stderr})")
                continue

            output_rows = count_csv_rows(output_path)
            if output_rows > 0:
                bypassed_files.append(f"{filename} ({output_rows} rows bypassed)")

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")

def test_experiment_log_updated():
    assert os.path.isfile(LOG_PATH), f"Experiment log missing at {LOG_PATH}"

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "Experiment log is empty."

    for i, line in enumerate(lines):
        try:
            entry = json.loads(line)
            assert "input_file" in entry, f"Missing 'input_file' in log entry {i+1}"
            assert "accepted" in entry, f"Missing 'accepted' in log entry {i+1}"
            assert "rejected" in entry, f"Missing 'rejected' in log entry {i+1}"
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in log entry {i+1}: {line}")