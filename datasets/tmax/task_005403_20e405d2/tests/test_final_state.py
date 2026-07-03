# test_final_state.py

import os
import subprocess
import csv
import pytest

def test_extracted_frames():
    frames_dir = "/home/user/extracted_frames"
    assert os.path.isdir(frames_dir), f"Extracted frames directory is missing: {frames_dir}"

    frames = [f for f in os.listdir(frames_dir) if f.endswith(".jpg")]
    assert len(frames) == 60, f"Expected 60 extracted frames, found {len(frames)}"

    # Check naming convention
    for frame in frames:
        assert frame.startswith("frame_") and frame.endswith(".jpg"), f"Invalid frame name: {frame}"

def test_classifier_script_exists():
    script_path = "/home/user/detect_corruption.py"
    assert os.path.isfile(script_path), f"Classifier script is missing: {script_path}"

def test_adversarial_corpus_classification():
    script_path = "/home/user/detect_corruption.py"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".jpg")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".jpg")]

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True, text=True)
        if "CLEAN" not in result.stdout.strip().upper():
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True, text=True)
        if "EVIL" not in result.stdout.strip().upper():
            evil_failures.append(os.path.basename(f))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (failed to return CLEAN): {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (failed to return EVIL): {', '.join(evil_failures)}")

    assert not error_msg, " | ".join(error_msg)

def test_frame_report():
    report_path = "/home/user/frame_report.csv"
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    with open(report_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Report is empty"
    assert rows[0] == ["filename", "status"], f"Invalid header: {rows[0]}"

    data_rows = rows[1:]
    assert len(data_rows) == 60, f"Expected 60 data rows in report, found {len(data_rows)}"

    for row in data_rows:
        assert len(row) == 2, f"Invalid row format: {row}"
        assert row[0].startswith("frame_") and row[0].endswith(".jpg"), f"Invalid filename in report: {row[0]}"
        assert row[1] in ["CLEAN", "EVIL"], f"Invalid status in report: {row[1]}"