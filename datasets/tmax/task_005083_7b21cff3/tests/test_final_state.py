# test_final_state.py

import os
import csv
import subprocess
import pytest
import sqlite3

def test_adversarial_corpus():
    script_path = "/home/user/validate.py"
    assert os.path.isfile(script_path), f"Validation script missing: {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_filled_metrics_csv():
    filled_path = "/home/user/filled_metrics.csv"
    assert os.path.isfile(filled_path), f"Filled metrics missing: {filled_path}"

    with open(filled_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['frame_index', 'intensity'], "Incorrect header in filled_metrics.csv"

        rows = list(reader)
        assert len(rows) == 30, "filled_metrics.csv should have exactly 30 data rows"

        for i, row in enumerate(rows):
            assert int(row[0]) == i, f"Expected frame_index {i}, got {row[0]}"
            intensity = float(row[1])
            assert 0.0 <= intensity <= 255.0, f"Intensity out of bounds: {intensity}"

def test_summary_csv():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Summary CSV missing: {summary_path}"

    with open(summary_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['window_start', 'avg_intensity'], "Incorrect header in summary.csv"

        rows = list(reader)
        assert len(rows) == 3, "summary.csv should have exactly 3 data rows"

        expected_starts = [0, 10, 20]
        for i, row in enumerate(rows):
            assert int(row[0]) == expected_starts[i], f"Expected window_start {expected_starts[i]}, got {row[0]}"

def test_cron_schedule():
    cron_path = "/home/user/cron_schedule.txt"
    assert os.path.isfile(cron_path), f"Cron schedule file missing: {cron_path}"

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Check for hourly execution of aggregate.sh
    assert "0 * * * *" in content, "Cron expression should run every hour on the hour (0 * * * *)"
    assert "/home/user/aggregate.sh" in content, "Cron expression should execute /home/user/aggregate.sh"