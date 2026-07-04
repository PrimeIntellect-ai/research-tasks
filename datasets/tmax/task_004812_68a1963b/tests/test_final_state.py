# test_final_state.py

import os
import json
import math

def test_dataset_bin():
    dataset_path = "/home/user/dataset.bin"
    assert os.path.isfile(dataset_path), "dataset.bin was not found in /home/user/"

    # Read corpus to determine exact number of tokens
    corpus_path = "/home/user/corpus.txt"
    assert os.path.isfile(corpus_path), "corpus.txt is missing"
    with open(corpus_path, "r") as f:
        text = f.read().strip()

    tokens = text.split(" ") if text else []
    expected_size = len(tokens) * 4

    actual_size = os.path.getsize(dataset_path)
    assert actual_size == expected_size, f"dataset.bin size is {actual_size} bytes, expected {expected_size} bytes (int32 = 4 bytes per token)"

def test_metrics_json():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), "metrics.json was not found in /home/user/"

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, "metrics.json is not valid JSON"

    assert "total_tokens" in metrics, "metrics.json is missing 'total_tokens'"
    assert "output_mean" in metrics, "metrics.json is missing 'output_mean'"
    assert "output_std" in metrics, "metrics.json is missing 'output_std'"

    # Read corpus to determine exact number of tokens
    corpus_path = "/home/user/corpus.txt"
    with open(corpus_path, "r") as f:
        text = f.read().strip()
    tokens = text.split(" ") if text else []
    expected_tokens = len(tokens)

    assert metrics["total_tokens"] == expected_tokens, f"Expected total_tokens to be {expected_tokens}, got {metrics['total_tokens']}"

    # Expected values derived from PyTorch model with manual_seed(42)
    expected_mean = 0.1770634651184082
    expected_std = 0.22276535630226135

    actual_mean = float(metrics["output_mean"])
    actual_std = float(metrics["output_std"])

    assert math.isclose(actual_mean, expected_mean, abs_tol=1e-4), f"output_mean {actual_mean} is not within 1e-4 of expected {expected_mean}"
    assert math.isclose(actual_std, expected_std, abs_tol=1e-4), f"output_std {actual_std} is not within 1e-4 of expected {expected_std}"