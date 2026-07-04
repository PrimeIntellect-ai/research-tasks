# test_final_state.py

import os
import subprocess
import csv
import pytest

def test_video_frames_csv():
    csv_path = "/home/user/video_frames.csv"
    assert os.path.exists(csv_path), f"Missing {csv_path}"

    # Generate expected data
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time,size", "-of", "csv=p=0",
        "/app/experiment_video.mp4"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    expected_rows = []
    for i, line in enumerate(result.stdout.strip().split('\n')):
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 2:
            expected_rows.append((str(i), parts[1].strip()))

    actual_rows = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[0] == "frame_index":
                continue
            actual_rows.append((row[0].strip(), row[1].strip()))

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}"
    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch: expected {expected}, got {actual}"

def test_wal_filter_executable():
    executable = "/home/user/wal_filter"
    assert os.path.exists(executable), f"Missing executable {executable}"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable"

def test_wal_filter_adversarial_corpus():
    executable = "/home/user/wal_filter"
    clean_dir = "/test_corpus/clean/"
    evil_dir = "/test_corpus/evil/"

    assert os.path.exists(clean_dir), f"Missing clean corpus dir {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing evil corpus dir {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run([executable, cf], capture_output=True, text=True)
        out = res.stdout.strip()
        if res.returncode != 0 or out != "CLEAN":
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run([executable, ef], capture_output=True, text=True)
        out = res.stdout.strip()
        # Pass if returns EVIL or non-zero exit code
        if res.returncode == 0 and out != "EVIL":
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_msgs, " ; ".join(error_msgs)