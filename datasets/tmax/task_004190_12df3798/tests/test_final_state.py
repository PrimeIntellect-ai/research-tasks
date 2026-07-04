# test_final_state.py

import os
import pytest

def test_manifest_f1_score():
    manifest_path = '/home/user/manifest.txt'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} not found."

    expected_paths = {
        "file1.txt",
        "dirA/file2.txt",
        "dirB/file3.txt"
    }

    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    found_paths = set()
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            # Get path and normalize by stripping leading /app/data/ or just taking the filename
            path = parts[2].replace('/app/data/', '')
            for ep in expected_paths:
                if path.endswith(ep):
                    found_paths.add(ep)

    true_positives = len(found_paths.intersection(expected_paths))
    false_positives = len(found_paths - expected_paths)
    false_negatives = len(expected_paths - found_paths)

    if true_positives == 0:
        f1 = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 score {f1:.2f} is below the threshold of 0.95. Found paths: {found_paths}, Expected paths: {expected_paths}"

def test_c_source_file_exists():
    c_source_path = '/home/user/generate_manifest.c'
    assert os.path.isfile(c_source_path), f"C source file {c_source_path} not found."