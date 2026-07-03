# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_raw_trajectory_exists_and_valid():
    """Check if raw_trajectory.csv is generated and has basic structure."""
    raw_path = "/home/user/pipeline/raw_trajectory.csv"
    assert os.path.isfile(raw_path), f"File missing: {raw_path}"

    with open(raw_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "raw_trajectory.csv is empty"
        assert len(header) >= 3, "raw_trajectory.csv should have at least 3 columns (frame_id, timestamp_ms, x_centroid)"

        rows = list(reader)
        assert len(rows) > 0, "raw_trajectory.csv has no data rows"

def test_clean_trajectory_exists_and_valid():
    """Check if clean_trajectory.csv is generated and has the required column."""
    clean_path = "/home/user/pipeline/clean_trajectory.csv"
    assert os.path.isfile(clean_path), f"File missing: {clean_path}"

    with open(clean_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "clean_trajectory.csv is empty"
        assert "x_smoothed_normalized" in header, "clean_trajectory.csv missing 'x_smoothed_normalized' column"

        rows = list(reader)
        assert len(rows) > 0, "clean_trajectory.csv has no data rows"

def test_detector_binary_exists():
    """Check if the detector binary is compiled and executable."""
    detector_path = "/home/user/bin/detector"
    assert os.path.isfile(detector_path), f"Detector binary missing: {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector binary is not executable: {detector_path}"

def test_detector_adversarial_corpus():
    """
    Run the detector against the clean and evil corpora.
    Clean corpus files must return exit code 0.
    Evil corpus files must return exit code > 0.
    """
    detector_path = "/home/user/bin/detector"
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isfile(detector_path), "Detector binary missing, cannot run corpus tests."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, f"Clean corpus directory {clean_dir} is empty or missing CSV files."
    assert len(evil_files) > 0, f"Evil corpus directory {evil_dir} is empty or missing CSV files."

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))