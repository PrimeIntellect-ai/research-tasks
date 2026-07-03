# test_final_state.py

import os
import subprocess
import pytest

def test_video_stats():
    stats_file = "/home/user/video_stats.txt"
    assert os.path.isfile(stats_file), f"Missing video stats file at {stats_file}"

    with open(stats_file, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Expected format 'total_frames,avg_intensity', got: {content}"

    try:
        total_frames = int(parts[0].strip())
        avg_intensity = float(parts[1].strip())
    except ValueError:
        pytest.fail(f"Could not parse integers/floats from video stats: {content}")

    assert total_frames == 150, f"Expected 150 frames, got {total_frames}"
    assert 111.0 <= avg_intensity <= 114.0, f"Expected average intensity around 112.4, got {avg_intensity}"

def test_classifier_compiled():
    classifier_path = "/home/user/classifier"
    assert os.path.isfile(classifier_path), f"Missing compiled classifier at {classifier_path}"
    assert os.access(classifier_path, os.X_OK), f"Classifier at {classifier_path} is not executable"

def run_classifier_and_get_predictions(target_dir):
    classifier_path = "/home/user/classifier"
    predictions_file = "predictions.txt"

    if os.path.exists(predictions_file):
        os.remove(predictions_file)

    result = subprocess.run([classifier_path, target_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Classifier failed on {target_dir} with error: {result.stderr}"

    assert os.path.isfile(predictions_file), f"Classifier did not produce {predictions_file} for {target_dir}"

    predictions = {}
    with open(predictions_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                predictions[parts[0].strip()] = parts[1].strip()

    return predictions

def test_classifier_clean_corpus():
    clean_dir = "/app/hidden_test/clean/"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"

    csv_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(csv_files) > 0, f"No CSV files found in {clean_dir}"

    predictions = run_classifier_and_get_predictions(clean_dir)

    modified = []
    for f in csv_files:
        if f not in predictions:
            modified.append(f"{f} (missing prediction)")
        elif predictions[f] != "0":
            modified.append(f"{f} (predicted {predictions[f]})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(csv_files)} clean modified/rejected. Offending files: {', '.join(modified[:10])}")

def test_classifier_evil_corpus():
    evil_dir = "/app/hidden_test/evil/"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    csv_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(csv_files) > 0, f"No CSV files found in {evil_dir}"

    predictions = run_classifier_and_get_predictions(evil_dir)

    bypassed = []
    for f in csv_files:
        if f not in predictions:
            bypassed.append(f"{f} (missing prediction)")
        elif predictions[f] != "1":
            bypassed.append(f"{f} (predicted {predictions[f]})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(csv_files)} evil bypassed. Offending files: {', '.join(bypassed[:10])}")