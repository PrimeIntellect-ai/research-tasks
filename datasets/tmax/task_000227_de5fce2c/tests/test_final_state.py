# test_final_state.py

import os
import subprocess
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_batch_score_script_exists():
    script_path = "/home/user/batch_score.py"
    assert os.path.exists(script_path), f"Agent script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."

def test_batch_score_accuracy():
    script_path = "/home/user/batch_score.py"
    input_csv = "/app/hidden_test_pairs.csv"
    output_csv = "/home/user/predictions.csv"
    truth_csv = "/app/hidden_expected_scores.csv"

    # Run the agent's script
    try:
        subprocess.run(
            ["python3", script_path, input_csv, output_csv],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"Agent script failed to run. Stderr: {e.stderr}"

    assert os.path.exists(output_csv), f"Output file {output_csv} was not created."

    try:
        preds = pd.read_csv(output_csv, header=None, names=["A", "B", "score"])
    except Exception as e:
        assert False, f"Failed to read output CSV {output_csv}: {e}"

    try:
        truth = pd.read_csv(truth_csv, header=None, names=["A", "B", "score"])
    except Exception as e:
        assert False, f"Failed to read truth CSV {truth_csv}: {e}"

    # Merge to ensure alignment
    merged = pd.merge(truth, preds, on=["A", "B"], suffixes=("_true", "_pred"))

    assert len(merged) == len(truth), f"Output CSV does not contain all expected pairs. Expected {len(truth)}, found {len(merged)} matching pairs."

    mse = mean_squared_error(merged["score_true"], merged["score_pred"])

    threshold = 0.001
    assert mse < threshold, f"MSE {mse:.6f} is not less than the threshold {threshold}."