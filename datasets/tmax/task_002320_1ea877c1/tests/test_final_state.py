# test_final_state.py

import os
import pytest

def load_set(path):
    with open(path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def test_f1_score():
    pred_path = '/home/user/clean_corpus.txt'
    gold_path = '/tmp/golden_corpus.txt'

    assert os.path.isfile(pred_path), f"Output file {pred_path} is missing. Did you write the cleaned corpus to the correct path?"
    assert os.path.isfile(gold_path), f"Golden file {gold_path} is missing."

    pred = load_set(pred_path)
    gold = load_set(gold_path)

    tp = len(pred & gold)
    fp = len(pred - gold)
    fn = len(gold - pred)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.99, f"F1 score {f1:.4f} is below the threshold of 0.99. Precision: {precision:.4f}, Recall: {recall:.4f}"

def test_cargo_toml_fixed():
    cargo_toml_path = '/app/text-dedup-engine/Cargo.toml'
    assert os.path.isfile(cargo_toml_path), f"{cargo_toml_path} is missing"
    with open(cargo_toml_path, 'r') as f:
        content = f.read()
    assert 'edition = "2099"' not in content, "Cargo.toml still has the perturbed edition '2099'. You need to fix the build issue."