# test_final_state.py

import os
import subprocess
import pytest

def test_video_ts_csv():
    csv_path = '/home/user/video_ts.csv'
    assert os.path.isfile(csv_path), f"Video telemetry CSV '{csv_path}' is missing."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 150, f"Expected exactly 150 rows in {csv_path}, but found {len(lines)}."

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Expected format 'timestamp,size', but got: '{line}'"
        try:
            float(parts[0])
            int(parts[1])
        except ValueError:
            pytest.fail(f"Invalid data types in row: '{line}'. Expected float,int.")

def test_ts_filter_corpus():
    executable = '/home/user/ts_filter'
    assert os.path.isfile(executable), f"Target executable '{executable}' is missing."
    assert os.access(executable, os.X_OK), f"Target executable '{executable}' is not executable."

    clean_dir = '/app/corpora/clean'
    evil_dir = '/app/corpora/evil'
    golden_dir = '/app/corpora/golden'

    # Verify clean corpus
    clean_failed = []
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    for fname in clean_files:
        in_path = os.path.join(clean_dir, fname)
        with open(in_path, 'r') as f_in:
            expected = f_in.read()

        proc = subprocess.run([executable, in_path], capture_output=True, text=True)
        if proc.returncode != 0 or proc.stdout != expected:
            clean_failed.append(fname)

    # Verify evil corpus
    evil_failed = []
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    for fname in evil_files:
        in_path = os.path.join(evil_dir, fname)
        golden_path = os.path.join(golden_dir, fname)
        with open(golden_path, 'r') as f_in:
            expected = f_in.read()

        proc = subprocess.run([executable, in_path], capture_output=True, text=True)
        if proc.returncode != 0 or proc.stdout != expected:
            evil_failed.append(fname)

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pipeline_script():
    script = '/home/user/pipeline.sh'
    assert os.path.isfile(script), f"Pipeline script '{script}' is missing."
    assert os.access(script, os.X_OK), f"Pipeline script '{script}' is not executable."

    in_path = '/app/corpora/clean/sensor_01.csv'
    proc = subprocess.run([script, in_path], capture_output=True, text=True)
    assert proc.returncode == 0, f"Pipeline script failed with exit code {proc.returncode}."

    lines = [line.strip() for line in proc.stdout.split('\n') if line.strip()]
    assert len(lines) > 0, "Pipeline script produced no output."

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 4, f"Expected joined format 'timestamp,sensor_id,value,size', but got: '{line}'"
        try:
            float(parts[0])
            float(parts[2])
            int(parts[3])
        except ValueError:
            pytest.fail(f"Invalid data types in joined pipeline output row: '{line}'")