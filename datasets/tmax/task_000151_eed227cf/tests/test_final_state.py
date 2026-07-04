# test_final_state.py

import os
import json
import subprocess
import glob
import pytest

FILTER_BIN = "/home/user/filter_bin"
PIPELINE_SH = "/home/user/pipeline.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
WINDOW_SIZE = 5

def run_filter(input_data):
    result = subprocess.run(
        [FILTER_BIN],
        input=input_data.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    return result.stdout.decode('utf-8')

def test_adversarial_corpus_filter():
    assert os.path.isfile(FILTER_BIN), f"Filter binary {FILTER_BIN} not found. Did you compile it?"
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary {FILTER_BIN} is not executable."

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))

    assert len(clean_files) > 0, "No files found in clean corpus directory."
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    clean_modified = []
    evil_bypassed = []

    # Test clean corpus
    for c_file in clean_files:
        with open(c_file, "r") as f:
            input_data = f.read()

        input_lines = [line for line in input_data.strip().split('\n') if line]

        try:
            output_data = run_filter(input_data)
        except subprocess.TimeoutExpired:
            clean_modified.append(os.path.basename(c_file))
            continue

        output_lines = [line for line in output_data.strip().split('\n') if line]

        if len(input_lines) != len(output_lines):
            clean_modified.append(os.path.basename(c_file))

    # Test evil corpus
    for e_file in evil_files:
        with open(e_file, "r") as f:
            input_data = f.read()

        try:
            output_data = run_filter(input_data)
        except subprocess.TimeoutExpired:
            # If it times out, we consider it not properly rejected (or crashed)
            evil_bypassed.append(os.path.basename(e_file))
            continue

        output_lines = [line for line in output_data.strip().split('\n') if line]

        # We expect 0 lines output for the evil corpus because all contain EXFIL
        if len(output_lines) > 0:
            evil_bypassed.append(os.path.basename(e_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (or dropped): {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_pipeline_rolling_average():
    assert os.path.isfile(PIPELINE_SH), f"Pipeline script {PIPELINE_SH} not found."
    assert os.access(PIPELINE_SH, os.X_OK), f"Pipeline script {PIPELINE_SH} is not executable."

    test_input_file = os.path.join(CLEAN_CORPUS_DIR, "clean.jsonl")
    assert os.path.isfile(test_input_file), f"Test input file {test_input_file} not found."

    # Read input to compute expected rolling average
    with open(test_input_file, "r") as f:
        lines = [line for line in f.read().strip().split('\n') if line]

    expected_rows = []
    byte_history = []
    for line in lines:
        record = json.loads(line)
        timestamp = record["timestamp"]
        bytes_val = record["bytes"]
        byte_history.append(bytes_val)

        window = byte_history[-WINDOW_SIZE:]
        avg = sum(window) / len(window)
        expected_rows.append(f"{timestamp},{bytes_val},{avg:.1f}")

    # Run pipeline
    result = subprocess.run(
        [PIPELINE_SH, test_input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10
    )

    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}\nStderr: {result.stderr.decode('utf-8')}"

    output_lines = [line for line in result.stdout.decode('utf-8').strip().split('\n') if line]

    assert len(output_lines) > 0, "Pipeline script produced no output."

    header = output_lines[0]
    assert header == "timestamp,bytes,rolling_avg_bytes", f"Incorrect CSV header: {header}"

    data_lines = output_lines[1:]
    assert len(data_lines) == len(expected_rows), f"Expected {len(expected_rows)} data rows, got {len(data_lines)}"

    for i, (actual, expected) in enumerate(zip(data_lines, expected_rows)):
        # Allow some float formatting flexibility
        actual_parts = actual.split(',')
        expected_parts = expected.split(',')

        assert len(actual_parts) == 3, f"Row {i+1} does not have 3 columns: {actual}"
        assert actual_parts[0] == expected_parts[0], f"Row {i+1} timestamp mismatch: {actual_parts[0]} != {expected_parts[0]}"
        assert actual_parts[1] == expected_parts[1], f"Row {i+1} bytes mismatch: {actual_parts[1]} != {expected_parts[1]}"

        actual_avg = float(actual_parts[2])
        expected_avg = float(expected_parts[2])
        assert abs(actual_avg - expected_avg) < 0.1, f"Row {i+1} rolling average mismatch: {actual_avg} != {expected_avg}"