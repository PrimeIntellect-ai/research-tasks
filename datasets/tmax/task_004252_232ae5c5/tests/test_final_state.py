# test_final_state.py
import os
import csv
import subprocess
import pytest

def test_frame_scores_csv():
    path = "/home/user/frame_scores.csv"
    assert os.path.isfile(path), f"Missing frame_scores.csv at {path}"

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "frame_scores.csv is empty"

        expected_cols = ["frame_index", "timestamp_sec", "visibility_score"]
        for col in expected_cols:
            assert col in header, f"Column '{col}' missing from frame_scores.csv header"

        rows = list(reader)
        assert len(rows) > 0, "frame_scores.csv has no data rows"

def test_merged_data_csv():
    path = "/home/user/merged_data.csv"
    assert os.path.isfile(path), f"Missing merged_data.csv at {path}"

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "merged_data.csv is empty"
        rows = list(reader)
        assert len(rows) > 0, "merged_data.csv has no data rows"

def test_filter_plots_clean_corpus():
    script_path = "/home/user/filter_plots.py"
    assert os.path.isfile(script_path), f"Missing filter_plots.py at {script_path}"

    clean_dir = "/app/verifier/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    expected_files = {f for f in os.listdir(clean_dir) if f.endswith('.png')}
    assert expected_files, "No PNG files found in clean corpus"

    result = subprocess.run(["python3", script_path, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"filter_plots.py failed on clean corpus:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    rejected_files = []
    processed_files = set()

    for line in output_lines:
        if ": " not in line:
            continue
        filename, status = line.split(": ", 1)
        if filename in expected_files:
            processed_files.add(filename)
            if status != "ACCEPT":
                rejected_files.append(filename)

    missing_files = expected_files - processed_files
    assert not missing_files, f"filter_plots.py did not output status for {len(missing_files)} clean files: {missing_files}"
    assert not rejected_files, f"{len(rejected_files)} of {len(expected_files)} clean files modified/rejected: {rejected_files}"

def test_filter_plots_evil_corpus():
    script_path = "/home/user/filter_plots.py"
    assert os.path.isfile(script_path), f"Missing filter_plots.py at {script_path}"

    evil_dir = "/app/verifier/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    expected_files = {f for f in os.listdir(evil_dir) if f.endswith('.png')}
    assert expected_files, "No PNG files found in evil corpus"

    result = subprocess.run(["python3", script_path, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"filter_plots.py failed on evil corpus:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    accepted_files = []
    processed_files = set()

    for line in output_lines:
        if ": " not in line:
            continue
        filename, status = line.split(": ", 1)
        if filename in expected_files:
            processed_files.add(filename)
            if status != "REJECT":
                accepted_files.append(filename)

    missing_files = expected_files - processed_files
    assert not missing_files, f"filter_plots.py did not output status for {len(missing_files)} evil files: {missing_files}"
    assert not accepted_files, f"{len(accepted_files)} of {len(expected_files)} evil files bypassed/accepted: {accepted_files}"