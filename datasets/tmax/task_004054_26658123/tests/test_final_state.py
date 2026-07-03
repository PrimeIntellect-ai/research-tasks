# test_final_state.py
import os
import json
import math
import subprocess
import pytest

def test_consolidated_parquet_exists():
    parquet_path = "/home/user/experiment_data/processed/consolidated.parquet"
    assert os.path.isfile(parquet_path), f"Parquet file missing at {parquet_path}"

def test_correlations_json_correctness():
    results_path = "/home/user/experiment_data/results/correlations.json"
    assert os.path.isfile(results_path), f"Correlations JSON missing at {results_path}"

    with open(results_path, "r") as f:
        try:
            student_correlations = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Correlations file is not valid JSON.")

    # Compute expected correlations directly from the raw data and weights
    raw_dir = "/home/user/experiment_data/raw"
    model_path = "/home/user/experiment_data/model/architecture_and_weights.json"

    assert os.path.isfile(model_path), "Original model weights missing."

    with open(model_path, "r") as f:
        weights = json.load(f)

    hw = weights["hidden.weight"]
    hb = weights["hidden.bias"]
    ow = weights["output.weight"]
    ob = weights["output.bias"]

    # Read and concatenate all CSVs in order
    all_data = []
    for i in range(50):
        csv_path = os.path.join(raw_dir, f"sim_{i}.csv")
        assert os.path.isfile(csv_path), f"Missing original CSV {csv_path}"
        with open(csv_path, "r") as f:
            for line in f:
                if line.strip():
                    all_data.append([float(x) for x in line.strip().split(",")])

    # Manual inference
    predictions = []
    for row in all_data:
        # Hidden layer: x @ hw.T + hb
        hidden_out = []
        for i in range(len(hw)):
            val = sum(row[j] * hw[i][j] for j in range(len(row))) + hb[i]
            # ReLU
            hidden_out.append(max(0.0, val))

        # Output layer: hidden_out @ ow.T + ob
        out_val = sum(hidden_out[j] * ow[0][j] for j in range(len(hidden_out))) + ob[0]
        predictions.append(out_val)

    # Compute Pearson correlation
    n = len(all_data)
    mean_p = sum(predictions) / n
    var_p = sum((p - mean_p) ** 2 for p in predictions)

    expected_correlations = {}
    for i in range(20):
        feat_vals = [row[i] for row in all_data]
        mean_f = sum(feat_vals) / n
        var_f = sum((f - mean_f) ** 2 for f in feat_vals)

        cov = sum((feat_vals[k] - mean_f) * (predictions[k] - mean_p) for k in range(n))
        corr = cov / math.sqrt(var_f * var_p) if var_f * var_p > 0 else 0.0
        expected_correlations[f"feature_{i}"] = round(corr, 4)

    # Compare
    for i in range(20):
        feat_name = f"feature_{i}"
        assert feat_name in student_correlations, f"Missing {feat_name} in output JSON."
        expected = expected_correlations[feat_name]
        actual = student_correlations[feat_name]
        assert abs(actual - expected) <= 0.0002, \
            f"Mismatch in {feat_name}. Expected {expected}, got {actual}"

def test_verify_pipeline_script():
    script_path = "/home/user/experiment_data/verify_pipeline.py"
    assert os.path.isfile(script_path), f"Verification script missing at {script_path}"

    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"verify_pipeline.py failed with exit code {result.returncode}.\nStderr: {result.stderr}"