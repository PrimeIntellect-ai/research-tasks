# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_final_report_mse():
    report_path = "/home/user/final_report.csv"
    assert os.path.exists(report_path), f"Final report file {report_path} is missing."

    try:
        df = pd.read_csv(report_path)
    except Exception as e:
        assert False, f"Failed to read {report_path} as CSV: {e}"

    assert 'Anomaly_Time_sec' in df.columns, f"'Anomaly_Time_sec' column is missing in {report_path}."

    pred = np.sort(df['Anomaly_Time_sec'].values)
    truth = np.array([12.45, 45.12, 89.33])

    if len(pred) != len(truth):
        mse = 999.0
        assert False, f"Expected {len(truth)} anomalies, but found {len(pred)}. MSE penalty applied."
    else:
        mse = np.mean((pred - truth)**2)

    assert mse <= 0.05, f"MSE {mse:.4f} is greater than the threshold of 0.05. Predictions: {pred}"