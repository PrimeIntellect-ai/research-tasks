# test_final_state.py
import os
import subprocess
import pandas as pd
from sklearn.metrics import f1_score

def test_predict_script_exists():
    """Check if the user created the predict.py script."""
    assert os.path.isfile("/home/user/predict.py"), "The script /home/user/predict.py does not exist."

def test_prediction_performance():
    """Run the prediction script and evaluate the F1 score."""
    predict_script = "/home/user/predict.py"
    test_audio = "/app/hidden_test.wav"
    output_csv = "/home/user/predictions.csv"
    truth_csv = "/app/hidden_truth.csv"

    # Ensure required hidden files exist (they should be mounted by the testing framework)
    assert os.path.isfile(test_audio), f"Hidden test audio {test_audio} missing."
    assert os.path.isfile(truth_csv), f"Hidden truth csv {truth_csv} missing."
    assert os.path.isfile("/app/test_segments.csv"), "Hidden test segments /app/test_segments.csv missing."

    # Run the user's prediction script
    result = subprocess.run(
        ["python3", predict_script, test_audio, output_csv],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"predict.py failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(output_csv), f"The script did not create the output file {output_csv}."

    # Read predictions and ground truth
    try:
        y_pred = pd.read_csv(output_csv, header=None).values.flatten()
    except Exception as e:
        raise AssertionError(f"Failed to read predictions from {output_csv}: {e}")

    try:
        y_true = pd.read_csv(truth_csv, header=None).values.flatten()
    except Exception as e:
        raise AssertionError(f"Failed to read truth from {truth_csv}: {e}")

    assert len(y_pred) == len(y_true), f"Expected {len(y_true)} predictions, got {len(y_pred)}."

    # Compute F1 Macro score
    score = f1_score(y_true, y_pred, average='macro')

    threshold = 0.80
    assert score >= threshold, f"Macro F1 Score is {score:.4f}, which is below the threshold of {threshold}."