# test_final_state.py

import os
import re
import pytest

def test_virtual_environment_exists():
    venv_python = '/home/user/ml_env/bin/python'
    assert os.path.isfile(venv_python), f"Virtual environment python not found at {venv_python}"

def test_directories_and_files_moved():
    normal_dir = '/home/user/data/normal'
    anomalies_dir = '/home/user/data/anomalies'
    samples_dir = '/home/user/data/samples'

    assert os.path.isdir(normal_dir), f"Directory not found: {normal_dir}"
    assert os.path.isdir(anomalies_dir), f"Directory not found: {anomalies_dir}"

    expected_normal = ['sample_1.csv', 'sample_3.csv', 'sample_5.csv']
    expected_anomalies = ['sample_2.csv', 'sample_4.csv']

    for filename in expected_normal:
        path = os.path.join(normal_dir, filename)
        assert os.path.isfile(path), f"Expected normal file missing: {path}"

    for filename in expected_anomalies:
        path = os.path.join(anomalies_dir, filename)
        assert os.path.isfile(path), f"Expected anomaly file missing: {path}"

    # Check that samples dir is empty
    remaining_samples = os.listdir(samples_dir)
    assert len(remaining_samples) == 0, f"Expected {samples_dir} to be empty, but found: {remaining_samples}"

def test_summary_file():
    summary_path = '/home/user/summary.txt'
    assert os.path.isfile(summary_path), f"Summary file missing at {summary_path}"

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines in summary.txt, found {len(lines)}"

    # Check sorting
    filenames = []
    for line in lines:
        match = re.match(r'^(sample_\d\.csv):\s*(-?\d+\.\d{3})$', line)
        assert match, f"Line does not match expected format 'filename.csv: <mean_score>' with 3 decimal places: '{line}'"

        filename = match.group(1)
        score = float(match.group(2))
        filenames.append(filename)

        # Check score sign aligns with the expected classification
        if filename in ['sample_2.csv', 'sample_4.csv']:
            assert score < 0, f"Expected negative score for anomaly {filename}, got {score}"
        else:
            assert score >= 0, f"Expected non-negative score for normal {filename}, got {score}"

    # Verify alphabetical sorting
    assert filenames == sorted(filenames), "The lines in summary.txt are not sorted alphabetically by filename."