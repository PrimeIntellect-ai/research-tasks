# test_final_state.py

import os
import subprocess
import pandas as pd
from sklearn.metrics import mean_squared_error
import pytest

def test_model_exists():
    assert os.path.isfile("/home/user/latency_model.pkl"), "/home/user/latency_model.pkl is missing."

def test_predict_script_exists():
    assert os.path.isfile("/home/user/predict.py"), "/home/user/predict.py is missing."

def test_mse_metric():
    test_data_path = "/app/hidden_test_data.csv"
    assert os.path.isfile(test_data_path), f"{test_data_path} is missing."

    # Run the predict script
    result = subprocess.run(
        ["python3", "/home/user/predict.py", test_data_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"predict.py failed with error: {result.stderr}"

    predictions_text = result.stdout.strip().split('\n')
    assert len(predictions_text) > 0 and predictions_text[0] != '', "predict.py produced no output."

    try:
        preds = [float(x.strip()) for x in predictions_text if x.strip()]
    except ValueError:
        pytest.fail("Output of predict.py contains non-numeric values.")

    truth_df = pd.read_csv(test_data_path)
    assert 'network_latency' in truth_df.columns, "'network_latency' column missing in hidden test data."
    truth = truth_df['network_latency'].values

    assert len(preds) == len(truth), f"Number of predictions ({len(preds)}) does not match number of test samples ({len(truth)})."

    mse = mean_squared_error(truth, preds)
    assert mse < 0.25, f"MSE is {mse:.4f}, which is not less than the required threshold of 0.25."