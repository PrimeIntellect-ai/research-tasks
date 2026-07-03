# test_final_state.py

import os
import pytest

def test_model_c_exists():
    """Test that the C program source file exists."""
    model_c_path = "/home/user/src/model.c"
    assert os.path.isfile(model_c_path), f"File {model_c_path} is missing."

def test_pipeline_sh_exists_and_executable():
    """Test that the shell script exists and is executable."""
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"File {pipeline_path} is missing."
    assert os.access(pipeline_path, os.X_OK), f"File {pipeline_path} is not executable."

def test_accuracy_txt_content():
    """Test that accuracy.txt exists and contains the correct accuracy."""
    accuracy_path = "/home/user/accuracy.txt"
    assert os.path.isfile(accuracy_path), f"File {accuracy_path} is missing."

    features_path = "/home/user/data/features.csv"
    labels_path = "/home/user/data/labels.csv"

    # Compute expected accuracy dynamically
    features = {}
    if os.path.isfile(features_path):
        with open(features_path, "r") as f:
            lines = f.read().strip().split('\n')
            for line in lines[1:]:
                if not line.strip(): continue
                parts = line.split(',')
                fid = parts[0]
                x, y, z = map(float, parts[1:4])
                score = x * 0.5 + y * 0.3 + z * 0.2
                pred = 1 if score > 0.5 else 0
                features[fid] = pred

    labels = {}
    if os.path.isfile(labels_path):
        with open(labels_path, "r") as f:
            lines = f.read().strip().split('\n')
            for line in lines[1:]:
                if not line.strip(): continue
                parts = line.split(',')
                fid = parts[0]
                label = int(parts[1])
                labels[fid] = label

    if features and labels:
        matches = 0
        total = 0
        for fid, pred in features.items():
            if fid in labels:
                if pred == labels[fid]:
                    matches += 1
                total += 1
        expected_accuracy = (matches / total) * 100 if total > 0 else 0.0
        expected_text = f"Accuracy: {expected_accuracy:.2f}%"
    else:
        # Fallback to the truth value if files are missing or empty
        expected_text = "Accuracy: 90.00%"

    with open(accuracy_path, "r") as f:
        content = f.read().strip()

    assert content == expected_text, f"Expected '{expected_text}' in {accuracy_path}, but got '{content}'."