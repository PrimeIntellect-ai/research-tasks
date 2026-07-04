# test_final_state.py

import os
import subprocess
import csv
import json
import glob
import pytest

def test_telemetry_sanitizer_clean_corpus():
    script_path = "/home/user/filter_telemetry.py"
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    clean_files = glob.glob("/app/corpus/clean/*.json")
    assert clean_files, "No clean corpus files found"

    failed_files = []
    for fpath in clean_files:
        with open(fpath, 'r') as f:
            expected_lines = [line.strip() for line in f if line.strip()]

        result = subprocess.run(["python3", script_path, fpath], capture_output=True, text=True)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        if len(output_lines) != len(expected_lines):
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {failed_files}"

def test_telemetry_sanitizer_evil_corpus():
    script_path = "/home/user/filter_telemetry.py"
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    evil_files = glob.glob("/app/corpus/evil/*.json")
    assert evil_files, "No evil corpus files found"

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True, text=True)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        if len(output_lines) > 0:
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}"

def test_video_etl_pipeline_output():
    csv_path = "/home/user/video_stats.csv"
    assert os.path.exists(csv_path), f"CSV output missing at {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ['frame_id', 'timestamp_sec', 'brightness', 'rolling_avg'], \
        f"Incorrect CSV columns: {reader.fieldnames}"

    assert len(rows) == 150, f"Expected 150 rows, got {len(rows)}"

    for i, row in enumerate(rows):
        assert int(row['frame_id']) == i, f"Expected frame_id {i}, got {row['frame_id']}"
        assert abs(float(row['timestamp_sec']) - (i / 30.0)) < 0.1, f"Incorrect timestamp for frame {i}"

        # Check rolling average
        start_idx = max(0, i - 4)
        expected_rolling = sum(float(rows[j]['brightness']) for j in range(start_idx, i + 1)) / (i - start_idx + 1)
        assert abs(float(row['rolling_avg']) - expected_rolling) < 0.1, \
            f"Incorrect rolling average at frame {i}: expected {expected_rolling}, got {row['rolling_avg']}"

def test_cron_job_scheduled():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "No crontab found for the user"

    cron_lines = [line for line in result.stdout.splitlines() if not line.strip().startswith('#') and line.strip()]

    found = False
    for line in cron_lines:
        if "/home/user/process_video.py" in line:
            parts = line.split()
            if len(parts) >= 5:
                # Top of every hour: minute 0
                if parts[0] == "0" and parts[1] == "*":
                    found = True
                    break

    assert found, "Cron job for /home/user/process_video.py at the top of every hour (minute 0) not found"