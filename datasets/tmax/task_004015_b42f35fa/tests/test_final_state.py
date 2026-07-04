# test_final_state.py

import os
import subprocess
import csv
import pytest

def test_frame_extraction_and_stats():
    frames_dir = "/home/user/frames"
    stats_file = "/home/user/frame_stats.csv"

    assert os.path.exists(frames_dir), f"Frames directory missing at {frames_dir}"
    assert os.path.isdir(frames_dir), f"{frames_dir} is not a directory"

    assert os.path.exists(stats_file), f"Stats file missing at {stats_file}"

    with open(stats_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Stats file is empty"
    header = rows[0]
    assert header == ['frame_number', 'mean_brightness'], f"Incorrect header: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 50, f"Expected 50 data rows, got {len(data_rows)}"

    # Check sorting
    frame_numbers = []
    for i, row in enumerate(data_rows):
        try:
            frame_num = int(row[0])
            frame_numbers.append(frame_num)
        except ValueError:
            pytest.fail(f"Invalid frame number at row {i+1}: {row[0]}")

    assert frame_numbers == sorted(frame_numbers), "frame_stats.csv is not sorted by frame number"

def test_filter_datasets_script_exists_and_executable():
    script_path = "/home/user/filter_datasets.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_adversarial_corpus_filtering():
    script_path = "/home/user/filter_datasets.sh"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    # Test clean corpus
    result_clean = subprocess.run(
        ["bash", script_path, clean_dir],
        capture_output=True,
        text=True
    )
    assert result_clean.returncode == 0, f"Script failed on clean dir with exit code {result_clean.returncode}"

    clean_output = result_clean.stdout.strip().split('\n') if result_clean.stdout.strip() else []
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]

    false_positives = [f for f in clean_output if any(cf in f for cf in clean_files)]
    assert len(false_positives) == 0, f"{len(false_positives)} of {len(clean_files)} clean files incorrectly flagged: {false_positives}"

    # Test evil corpus
    result_evil = subprocess.run(
        ["bash", script_path, evil_dir],
        capture_output=True,
        text=True
    )
    assert result_evil.returncode == 0, f"Script failed on evil dir with exit code {result_evil.returncode}"

    evil_output = result_evil.stdout.strip()
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]

    missed_evil = [f for f in evil_files if f not in evil_output]
    assert len(missed_evil) == 0, f"{len(missed_evil)} of {len(evil_files)} evil files bypassed detection: {missed_evil}"

def test_saved_results():
    clean_results_file = "/home/user/clean_results.txt"
    evil_results_file = "/home/user/evil_results.txt"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(clean_results_file), f"Missing {clean_results_file}"
    assert os.path.exists(evil_results_file), f"Missing {evil_results_file}"

    with open(clean_results_file, 'r') as f:
        clean_content = f.read().strip()
    assert clean_content == "", f"clean_results.txt should be empty, but contains: {clean_content}"

    with open(evil_results_file, 'r') as f:
        evil_content = f.read().strip()

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    missed = [f for f in evil_files if f not in evil_content]
    assert len(missed) == 0, f"evil_results.txt is missing evil files: {missed}"