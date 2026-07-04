# test_final_state.py
import os
import subprocess
import pandas as pd
from sklearn.metrics import roc_auc_score

def test_predict_script_and_roc_auc():
    script_path = '/home/user/predict.py'
    assert os.path.exists(script_path), f"Prediction script not found at {script_path}"

    test_csv = '/app/data/test.csv'
    output_csv = '/home/user/predictions.csv'

    # Run the prediction script
    result = subprocess.run(['python', script_path, test_csv, output_csv], capture_output=True, text=True)
    assert result.returncode == 0, f"Prediction script failed with error:\n{result.stderr}"

    assert os.path.exists(output_csv), f"Output CSV not found at {output_csv}"

    preds = pd.read_csv(output_csv)
    truth = pd.read_csv('/app/data/test_labels.csv')

    assert 'probability' in preds.columns, "Output CSV must contain a 'probability' column"

    auc = roc_auc_score(truth['target'], preds['probability'])
    assert auc >= 0.75, f"ROC-AUC {auc:.4f} is below threshold 0.75"