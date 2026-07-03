# test_final_state.py

import os
import subprocess
import pandas as pd
import numpy as np
import pytest

def test_final_features_csv_exists():
    target_csv = "/home/user/final_features.csv"
    assert os.path.exists(target_csv), f"{target_csv} does not exist. The pipeline must generate this file."

def test_cron_job_configured():
    try:
        cron_check = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure the cron job is configured for the user.")

    assert "run_pipeline.sh" in cron_check, "run_pipeline.sh is not scheduled in the user's crontab."

def test_metric_threshold():
    target_csv = "/home/user/final_features.csv"
    ref_csv = "/app/reference_features.csv"

    assert os.path.exists(target_csv), f"Target CSV missing: {target_csv}"
    assert os.path.exists(ref_csv), f"Reference CSV missing: {ref_csv}"

    try:
        df = pd.read_csv(target_csv)
    except Exception as e:
        pytest.fail(f"Failed to read {target_csv} as a CSV: {e}")

    try:
        ref_df = pd.read_csv(ref_csv)
    except Exception as e:
        pytest.fail(f"Failed to read {ref_csv} as a CSV: {e}")

    required_columns = ['frame_id', 'lang', 'repaired_text', 'r_avg', 'g_avg', 'b_avg']
    for col in required_columns:
        assert col in df.columns, f"Missing required column '{col}' in {target_csv}."

    merged = pd.merge(ref_df, df, on="frame_id", suffixes=('_ref', '_agent'))

    assert len(merged) > 0, "No matching frame_ids found between reference and agent output."

    # Text accuracy (percentage error)
    text_matches = (merged['repaired_text_ref'] == merged['repaired_text_agent']).sum()
    text_error_rate = (len(ref_df) - text_matches) / len(ref_df) * 100

    # RGB MSE
    mse_r = np.mean((merged['r_avg_ref'] - merged['r_avg_agent'])**2)
    mse_g = np.mean((merged['g_avg_ref'] - merged['g_avg_agent'])**2)
    mse_b = np.mean((merged['b_avg_ref'] - merged['b_avg_agent'])**2)

    total_mse = (mse_r + mse_g + mse_b) / 3.0

    combined_metric = text_error_rate + total_mse

    assert combined_metric <= 5.0, (
        f"Combined error score {combined_metric:.2f} exceeds threshold of 5.0. "
        f"Text Error Rate: {text_error_rate:.2f}%, Total RGB MSE: {total_mse:.2f}"
    )