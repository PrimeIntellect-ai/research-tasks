# test_final_state.py
import os
import subprocess
import pytest

def compute_expected_predictions():
    features_path = "/home/user/data/features.csv"
    metadata_path = "/home/user/data/metadata.csv"
    weights_path = "/home/user/models/v2_weights.txt"

    # Read weights
    with open(weights_path, "r") as f:
        w1, w2, w3, b = map(float, f.read().strip().split(","))

    # Read features
    features = {}
    with open(features_path, "r") as f:
        lines = f.read().strip().split("\n")[1:] # skip header
        for line in lines:
            parts = line.split(",")
            features[parts[0]] = list(map(float, parts[1:]))

    # Read metadata
    metadata = {}
    with open(metadata_path, "r") as f:
        lines = f.read().strip().split("\n")[1:] # skip header
        for line in lines:
            parts = line.split(",")
            metadata[parts[0]] = parts[2] # model_version

    # Compute predictions
    predictions = {}
    for pid in features:
        if pid in metadata and metadata[pid] == "v2":
            f1, f2, f3 = features[pid]
            val = w1*f1 + w2*f2 + w3*f3 + b
            predictions[pid] = max(0.0, val)

    return predictions

def test_pipeline_execution_and_output():
    script_path = "/home/user/run_pipeline.sh"
    cpp_path = "/home/user/infer.cpp"

    assert os.path.exists(cpp_path), f"Missing C++ file at {cpp_path}"
    assert os.path.exists(script_path), f"Missing script at {script_path}"

    # Run the pipeline
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_pipeline.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    predictions_path = "/home/user/predictions.csv"
    summary_path = "/home/user/summary.txt"

    assert os.path.exists(predictions_path), f"Predictions file not found at {predictions_path}"
    assert os.path.exists(summary_path), f"Summary file not found at {summary_path}"

    expected_preds = compute_expected_predictions()

    # Read actual predictions
    actual_preds = {}
    with open(predictions_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid prediction format: {line}"
            actual_preds[parts[0]] = float(parts[1])

    # Check predictions
    assert set(actual_preds.keys()) == set(expected_preds.keys()), "Prediction IDs do not match expected 'v2' rows."

    for pid, exp_val in expected_preds.items():
        act_val = actual_preds[pid]
        assert abs(act_val - exp_val) < 1e-4, f"Prediction for ID {pid} is {act_val}, expected {exp_val:.4f}"

    # Check summary
    expected_avg = sum(expected_preds.values()) / len(expected_preds)

    with open(summary_path, "r") as f:
        summary_content = f.read().strip()

    try:
        actual_avg = float(summary_content)
    except ValueError:
        pytest.fail(f"Summary file does not contain a valid float: {summary_content}")

    assert abs(actual_avg - expected_avg) < 1e-4, f"Summary average is {actual_avg}, expected {expected_avg:.4f}"