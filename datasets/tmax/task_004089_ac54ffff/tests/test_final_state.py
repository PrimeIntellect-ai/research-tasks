# test_final_state.py

import os
import json
import pytest

def calculate_f1(pred_manifest_path, true_manifest):
    try:
        with open(pred_manifest_path, 'r') as f:
            pred = json.load(f)
    except Exception:
        return 0.0

    pred_set = set(pred.keys())
    true_set = set(true_manifest.keys())

    tp = len(pred_set.intersection(true_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    if tp == 0: return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * (precision * recall) / (precision + recall)

def test_project_tarball_exists():
    tarball_path = "/home/user/project.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball missing at {tarball_path}"

def test_manifest_f1_score():
    manifest_path = "/home/user/organized_project/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    true_manifest = {
        "media/images/photo.jpg": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "docs/notes.md": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "src/script.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "logs/app.json": "..." 
    }

    f1 = calculate_f1(manifest_path, true_manifest)
    assert f1 >= 0.95, f"F1 score of manifest keys is {f1:.4f}, which is below the threshold of 0.95"