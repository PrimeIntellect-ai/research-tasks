# test_final_state.py

import os
import subprocess
import pandas as pd
import numpy as np
import scipy.stats as stats
from pathlib import Path

def test_surrogate_script_exists():
    script_path = Path("/home/user/surrogate.py")
    assert script_path.exists(), "The script /home/user/surrogate.py does not exist."
    assert script_path.is_file(), "/home/user/surrogate.py is not a file."

def test_mean_ci_correct():
    ci_path = Path("/home/user/mean_ci.txt")
    assert ci_path.exists(), "/home/user/mean_ci.txt does not exist."

    # Recompute the true scores for the original logs.csv
    logs_csv = "/home/user/logs.csv"
    assert Path(logs_csv).exists(), "/home/user/logs.csv is missing."

    true_scores_path = "/tmp/true_train_scores.csv"
    subprocess.run(['/app/risk_evaluator', logs_csv], stdout=open(true_scores_path, 'w'), check=True)

    df = pd.read_csv(true_scores_path)
    scores = df['risk_score'].values

    # Calculate 95% CI using t-distribution
    n = len(scores)
    mean = np.mean(scores)
    se = stats.sem(scores)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)

    expected_ci_str = f"[{ci[0]:.4f}, {ci[1]:.4f}]"

    with open(ci_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_ci_str, f"Expected CI: {expected_ci_str}, but found: {content}"

def test_surrogate_mse():
    # 1. Create test_logs.csv
    test_data = pd.DataFrame({
        'log_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'message': [
            'system error fail', 
            'warning high temp', 
            'success login', 
            'timeout error', 
            'fail fail fail',
            'no keywords here',
            'error warning success timeout fail',
            'ERROR uppercase',
            'multiple error error error',
            'success success'
        ]
    })
    test_csv = '/tmp/test_logs_eval.csv'
    test_data.to_csv(test_csv, index=False)

    # 2. Run oracle
    true_csv = '/tmp/true_scores_eval.csv'
    subprocess.run(['/app/risk_evaluator', test_csv], stdout=open(true_csv, 'w'), check=True)
    true_df = pd.read_csv(true_csv)

    # 3. Run agent script
    pred_csv = '/tmp/pred_scores_eval.csv'
    result = subprocess.run(['python3', '/home/user/surrogate.py', test_csv, pred_csv], capture_output=True, text=True)
    assert result.returncode == 0, f"Surrogate script failed with error:\n{result.stderr}"

    assert Path(pred_csv).exists(), f"Surrogate script did not create the output file {pred_csv}"
    pred_df = pd.read_csv(pred_csv)

    # 4. Compute MSE
    assert 'log_id' in pred_df.columns and 'predicted_score' in pred_df.columns, "Output CSV must contain 'log_id' and 'predicted_score' columns."

    merged = pd.merge(true_df, pred_df, on='log_id')
    assert len(merged) == len(true_df), "Mismatch in number of rows between true and predicted scores."

    mse = np.mean((merged['risk_score'] - merged['predicted_score'])**2)
    threshold = 0.05

    assert mse <= threshold, f"MSE is {mse:.4f}, which is greater than the threshold of {threshold}."