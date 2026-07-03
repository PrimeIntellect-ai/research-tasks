# test_final_state.py

import os
import json
import re
from collections import Counter
import pytest

SCRIPT_PATH = "/home/user/process_artifacts.sh"
SUMMARY_PATH = "/home/user/summary.json"
EXPERIMENTS_DIR = "/home/user/experiments"

def get_expected_metrics():
    accuracies = []
    losses = []
    words = []

    if not os.path.isdir(EXPERIMENTS_DIR):
        return 0.0, 0.0, []

    for fname in os.listdir(EXPERIMENTS_DIR):
        if not fname.endswith('.json'):
            continue
        filepath = os.path.join(EXPERIMENTS_DIR, fname)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                accuracies.append(data['metrics']['accuracy'])
                losses.append(data['metrics']['loss'])

                notes = data.get('notes', '').lower()
                # Strip out all characters except letters (a-z) and spaces
                notes_cleaned = re.sub(r'[^a-z\s]', '', notes)
                words.extend(notes_cleaned.split())
            except Exception:
                pass

    mean_acc = sum(accuracies) / len(accuracies) if accuracies else 0.0
    max_loss = max(losses) if losses else 0.0

    mean_acc = round(mean_acc, 2)
    max_loss = round(max_loss, 2)

    counter = Counter(words)
    top_tokens = counter.most_common(3)

    return mean_acc, max_loss, top_tokens

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_summary_json_exists_and_valid():
    """Check if summary.json exists and contains valid JSON."""
    assert os.path.isfile(SUMMARY_PATH), f"Output file {SUMMARY_PATH} does not exist."

    with open(SUMMARY_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_PATH} does not contain valid JSON.")

    assert "mean_accuracy" in data, "Key 'mean_accuracy' missing in summary.json"
    assert "max_loss" in data, "Key 'max_loss' missing in summary.json"
    assert "top_tokens" in data, "Key 'top_tokens' missing in summary.json"
    assert isinstance(data["top_tokens"], list), "'top_tokens' must be a list"

def test_summary_metrics_accuracy_and_loss():
    """Verify that mean_accuracy and max_loss are correctly calculated."""
    if not os.path.isfile(SUMMARY_PATH):
        pytest.skip("summary.json not found")

    with open(SUMMARY_PATH, 'r') as f:
        data = json.load(f)

    expected_mean_acc, expected_max_loss, _ = get_expected_metrics()

    actual_mean_acc = data.get("mean_accuracy")
    actual_max_loss = data.get("max_loss")

    assert isinstance(actual_mean_acc, (int, float)), "mean_accuracy must be a number"
    assert isinstance(actual_max_loss, (int, float)), "max_loss must be a number"

    assert abs(actual_mean_acc - expected_mean_acc) < 0.015, \
        f"Expected mean_accuracy ~{expected_mean_acc}, got {actual_mean_acc}"
    assert abs(actual_max_loss - expected_max_loss) < 0.015, \
        f"Expected max_loss ~{expected_max_loss}, got {actual_max_loss}"

def test_summary_top_tokens():
    """Verify that the top tokens are correctly extracted and sorted."""
    if not os.path.isfile(SUMMARY_PATH):
        pytest.skip("summary.json not found")

    with open(SUMMARY_PATH, 'r') as f:
        data = json.load(f)

    _, _, expected_top_tokens = get_expected_metrics()
    actual_top_tokens = data.get("top_tokens", [])

    assert len(actual_top_tokens) == 3, f"Expected exactly 3 top tokens, got {len(actual_top_tokens)}"

    # Check structure of each token object
    for item in actual_top_tokens:
        assert "token" in item, "Missing 'token' key in top_tokens item"
        assert "count" in item, "Missing 'count' key in top_tokens item"

    # Check descending order
    counts = [item["count"] for item in actual_top_tokens]
    assert counts == sorted(counts, reverse=True), "top_tokens is not sorted in descending order of frequency"

    # Create dictionaries for comparison
    expected_dict = {k: v for k, v in expected_top_tokens}
    actual_dict = {item["token"]: item["count"] for item in actual_top_tokens}

    for token, count in expected_dict.items():
        assert token in actual_dict, f"Expected token '{token}' not found in top_tokens"
        assert actual_dict[token] == count, f"Expected count {count} for token '{token}', got {actual_dict[token]}"