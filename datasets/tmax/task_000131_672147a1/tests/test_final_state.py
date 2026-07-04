# test_final_state.py

import os
import subprocess
import csv
import pytest

def test_extracted_trajectory():
    csv_path = "/home/user/extracted_trajectory.csv"
    assert os.path.exists(csv_path), f"Missing extracted trajectory CSV at {csv_path}"

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"

    header = rows[0]
    expected_header = ["frame_id", "x", "y"]
    assert [c.strip() for c in header] == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 100, f"Expected 100 data rows, got {len(data_rows)}"

    for i, row in enumerate(data_rows):
        assert len(row) == 3, f"Row {i} has incorrect number of columns: {row}"
        frame_id, x, y = row
        assert frame_id.strip().isdigit(), f"Row {i} frame_id is not an integer: {frame_id}"
        assert x.strip().lstrip('-').isdigit(), f"Row {i} x is not an integer: {x}"
        assert y.strip().lstrip('-').isdigit(), f"Row {i} y is not an integer: {y}"

def test_pipeline_clean_corpus():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.exists(pipeline_script), f"Missing pipeline script at {pipeline_script}"
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script {pipeline_script} is not executable"

    clean_dir = "/app/corpora/clean/"
    result = subprocess.run([pipeline_script, clean_dir], capture_output=True, text=True)

    # Check that it executed successfully
    assert result.returncode == 0, f"Pipeline script failed on clean corpus with error: {result.stderr}"

    output_lines = result.stdout.strip().split('\n')

    # We expect output lines like "filename: CLEAN"
    evil_count = sum(1 for line in output_lines if "EVIL" in line)
    clean_count = sum(1 for line in output_lines if "CLEAN" in line)

    evil_files = [line for line in output_lines if "EVIL" in line]

    assert evil_count == 0, f"{evil_count} of {len(output_lines)} clean files were incorrectly classified as EVIL. Offending files: {evil_files}"
    assert clean_count >= 50, f"Expected at least 50 clean files classified, got {clean_count}"

def test_pipeline_evil_corpus():
    pipeline_script = "/home/user/pipeline.sh"
    evil_dir = "/app/corpora/evil/"

    result = subprocess.run([pipeline_script, evil_dir], capture_output=True, text=True)

    assert result.returncode == 0, f"Pipeline script failed on evil corpus with error: {result.stderr}"

    output_lines = result.stdout.strip().split('\n')

    clean_count = sum(1 for line in output_lines if "CLEAN" in line)
    evil_count = sum(1 for line in output_lines if "EVIL" in line)

    clean_files = [line for line in output_lines if "CLEAN" in line]

    assert clean_count == 0, f"{clean_count} of {len(output_lines)} evil files bypassed the filter and were classified as CLEAN. Offending files: {clean_files}"
    assert evil_count >= 50, f"Expected at least 50 evil files classified, got {evil_count}"

def test_frames_extracted():
    frames_dir = "/home/user/frames/"
    assert os.path.exists(frames_dir), f"Missing frames directory at {frames_dir}"

    pgm_files = [f for f in os.listdir(frames_dir) if f.endswith(".pgm")]
    assert len(pgm_files) == 100, f"Expected 100 PGM files in {frames_dir}, got {len(pgm_files)}"