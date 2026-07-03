# test_final_state.py

import os
import pandas as pd
import pytest

def test_simdjson_fixed():
    """Verify that the deliberate perturbation in simdjson's CMakeLists.txt was fixed."""
    cmake_path = "/app/simdjson/CMakeLists.txt"
    if os.path.isfile(cmake_path):
        with open(cmake_path, "r") as f:
            content = f.read()
        assert "CMAKE_CXX_STANDARD 11" not in content, "simdjson CMakeLists.txt still contains the legacy 'CMAKE_CXX_STANDARD 11' perturbation."

def test_executable_exists():
    """Check if the compiled C++ executable is present and executable."""
    executable_path = "/home/user/bin/config_tracker"
    assert os.path.isfile(executable_path), f"Executable missing at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable."

def test_output_file_exists():
    """Check if the anomalies CSV output is present."""
    output_path = "/home/user/output/anomalies.csv"
    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

def test_f1_score_metric():
    """Evaluate the F1-score of the generated anomalies against the ground truth."""
    output_path = "/home/user/output/anomalies.csv"
    truth_path = "/tmp/ground_truth.csv"

    assert os.path.isfile(output_path), "Cannot evaluate F1-score: output file missing."
    assert os.path.isfile(truth_path), "Ground truth file missing."

    try:
        pred = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read predictions CSV: {e}")

    try:
        truth = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read truth CSV: {e}")

    assert 'server_id' in pred.columns and 'window_start' in pred.columns, \
        "Output CSV must contain 'server_id' and 'window_start' columns."

    pred_set = set(zip(pred['server_id'], pred['window_start']))
    truth_set = set(zip(truth['server_id'], truth['window_start']))

    true_positives = len(pred_set & truth_set)
    false_positives = len(pred_set - truth_set)
    false_negatives = len(truth_set - pred_set)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    threshold = 0.98
    assert f1 >= threshold, f"F1 Score {f1:.4f} is below the required threshold of {threshold}. (Precision: {precision:.4f}, Recall: {recall:.4f})"