# test_final_state.py

import os
import json
import pytest

def test_fast_vocab_installed():
    """Check if the fast_vocab package was successfully installed and fixed."""
    try:
        import fast_vocab
        from fast_vocab.tokenizer import tokenize
    except ImportError as e:
        pytest.fail(f"Failed to import fast_vocab: {e}. The package was not installed correctly.")
    except SyntaxError as e:
        pytest.fail(f"SyntaxError when importing fast_vocab: {e}. The syntax error was not fixed.")

    # Test that tokenizer works
    try:
        result = tokenize("hello world")
        assert isinstance(result, str), "tokenize should return a string"
    except Exception as e:
        pytest.fail(f"fast_vocab.tokenize failed to execute: {e}")

def test_oob_accuracies_file():
    """Check if the OOB accuracies file exists and has 200 lines."""
    path = "/home/user/oob_accuracies.csv"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        lines = f.readlines()

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    assert len(lines) == 200, f"Expected 200 OOB accuracy scores, found {len(lines)}."

    # Check if they are valid floats
    for line in lines:
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Invalid float in {path}: {line}")

def test_experiment_results_json():
    """Check if the experiment results JSON exists and contains the required keys."""
    path = "/home/user/experiment_results.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {path}: {e}")

    required_keys = ["mean", "ci_lower", "ci_upper"]
    for key in required_keys:
        assert key in data, f"Key '{key}' is missing from {path}."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

def test_metric_threshold():
    """Verify that the mean OOB accuracy is >= 0.70."""
    path = "/home/user/experiment_results.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        data = json.load(f)

    mean_acc = data.get('mean', 0.0)
    assert mean_acc >= 0.70, f"Failed: Mean accuracy {mean_acc} is below 0.70 threshold."