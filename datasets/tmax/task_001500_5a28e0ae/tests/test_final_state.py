# test_final_state.py
import os
import glob
import json
import math
import subprocess
import pytest

def get_expected_records(filepath):
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Deduplicate by sensor_id, keeping highest timestamp
    latest = {}
    for r in records:
        sid = r['sensor_id']
        if sid not in latest or r['timestamp'] > latest[sid]['timestamp']:
            latest[sid] = r

    deduped = list(latest.values())
    if not deduped:
        return []

    mean = sum(r['signal'] for r in deduped) / len(deduped)
    variance = sum((r['signal'] - mean) ** 2 for r in deduped) / len(deduped)
    stddev = math.sqrt(variance)

    surviving = []
    for r in deduped:
        if stddev == 0:
            surviving.append(r)
        else:
            z = abs((r['signal'] - mean) / stddev)
            if z <= 2.0:
                surviving.append(r)

    return surviving

def run_cleaner(filepath):
    executable = "/home/user/cleaner"
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you compile the Go program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

    result = subprocess.run([executable, filepath], capture_output=True, text=True)
    assert result.returncode == 0, f"Cleaner failed on {filepath} with error:\n{result.stderr}"

    output_records = []
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if line:
            try:
                output_records.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON output from cleaner on {filepath}: {line}")

    return output_records

def test_clean_corpus():
    clean_dir = "/app/corpus/clean"
    files = glob.glob(os.path.join(clean_dir, "*.jsonl"))
    assert files, f"No JSONL files found in {clean_dir}"

    failed_files = []
    for filepath in files:
        expected = get_expected_records(filepath)
        actual = run_cleaner(filepath)

        # Sort both lists of dicts by sensor_id for comparison
        expected_sorted = sorted(expected, key=lambda x: x['sensor_id'])
        actual_sorted = sorted(actual, key=lambda x: x['sensor_id'])

        if expected_sorted != actual_sorted:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} clean modified/rejected incorrectly. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_dir = "/app/corpus/evil"
    files = glob.glob(os.path.join(evil_dir, "*.jsonl"))
    assert files, f"No JSONL files found in {evil_dir}"

    failed_files = []
    for filepath in files:
        expected = get_expected_records(filepath)
        actual = run_cleaner(filepath)

        expected_sorted = sorted(expected, key=lambda x: x['sensor_id'])
        actual_sorted = sorted(actual, key=lambda x: x['sensor_id'])

        if expected_sorted != actual_sorted:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} evil bypassed/handled incorrectly. Offending files: {', '.join(failed_files)}")