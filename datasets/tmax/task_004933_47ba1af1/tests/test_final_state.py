# test_final_state.py

import os
import pandas as pd
import numpy as np

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script at {script_path} is not executable"

def test_results_csv_exists():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Results CSV not found at {results_path}"

def test_results_metric_threshold():
    results_path = "/home/user/results.csv"
    truth_path = "/app/.hidden_truth.csv"

    assert os.path.isfile(results_path), f"Results CSV missing: {results_path}"
    assert os.path.isfile(truth_path), f"Hidden truth CSV missing: {truth_path}"

    try:
        df_agent = pd.read_csv(results_path)
    except Exception as e:
        assert False, f"Failed to read {results_path} as CSV: {e}"

    try:
        df_truth = pd.read_csv(truth_path)
    except Exception as e:
        assert False, f"Failed to read {truth_path} as CSV: {e}"

    required_columns = ['time_sec', 'sensor_a', 'intensity', 'anomaly_flag']
    for col in required_columns:
        assert col in df_agent.columns, f"Missing required column '{col}' in {results_path}"

    # Merge to compare
    df_eval = pd.merge(df_truth, df_agent, on='time_sec', suffixes=('_true', '_pred'))

    assert not df_eval.empty, "Merged dataframe is empty. Ensure 'time_sec' matches the expected values."

    # Calculate Intensity MAE
    mae_intensity = np.abs(df_eval['intensity_pred'] - df_eval['intensity_true']).mean()

    # Calculate Anomaly Accuracy
    accuracy = (df_eval['anomaly_flag_pred'] == df_eval['anomaly_flag_true']).mean()

    # Calculate final score
    score = accuracy - (mae_intensity / 255.0)

    threshold = 0.85
    assert score >= threshold, f"Score {score:.4f} is below threshold {threshold} (Accuracy: {accuracy:.4f}, MAE: {mae_intensity:.4f})"