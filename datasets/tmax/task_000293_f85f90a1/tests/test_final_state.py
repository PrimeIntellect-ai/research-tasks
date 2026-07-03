# test_final_state.py

import os
import re
import subprocess
import pytest
import pandas as pd
import numpy as np

def test_toolkit_fixed():
    awk_script = "/app/awk-ts-tools-1.0/interpolate.awk"
    makefile = "/app/awk-ts-tools-1.0/Makefile"

    assert os.path.isfile(awk_script), f"Missing interpolate.awk at {awk_script}"
    with open(awk_script, "r") as f:
        awk_content = f.read()

    # The bug was `slope = (y2 + y1) / (x2 - x1)`
    # The fix should be `slope = (y2 - y1) / (x2 - x1)` or similar correct logic
    assert "slope = (y2 + y1)" not in awk_content, "The mathematical bug in interpolate.awk was not fixed."

    assert os.path.isfile(makefile), f"Missing Makefile at {makefile}"
    with open(makefile, "r") as f:
        makefile_content = f.read()
    assert "nonexistent-awk" not in makefile_content, "The AWK_BIN environment variable in the Makefile still points to a nonexistent awk."

def test_pipeline_script_exists():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_script), f"Pipeline script missing at {pipeline_script}"
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script {pipeline_script} is not executable."

def test_cron_job_configured():
    result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab for user 'user'"

    crontab_content = result.stdout.strip()

    # Check for every 15 minutes syntax: */15 or 0,15,30,45
    cron_pattern = re.compile(r'(?m)^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*.*(?:bash\s+)?/home/user/pipeline\.sh')
    assert cron_pattern.search(crontab_content) is not None, f"Cron job for pipeline.sh every 15 minutes not found in crontab:\n{crontab_content}"

def test_processed_data_mse():
    predicted_path = "/home/user/data/processed/master.csv"
    truth_path = "/tmp/ground_truth.csv"

    assert os.path.isfile(predicted_path), f"Processed master.csv missing at {predicted_path}"
    assert os.path.isfile(truth_path), f"Ground truth file missing at {truth_path}"

    try:
        pred_df = pd.read_csv(predicted_path, names=['timestamp', 'temperature'])
        truth_df = pd.read_csv(truth_path, names=['timestamp', 'temperature'])

        # Merge on timestamp to align data
        merged = pd.merge(truth_df, pred_df, on='timestamp', suffixes=('_truth', '_pred'))
        assert len(merged) > 0, "No matching timestamps found between predicted and ground truth data."

        mse = np.mean((merged['temperature_truth'] - merged['temperature_pred'])**2)
    except Exception as e:
        pytest.fail(f"Failed to calculate MSE: {e}")

    threshold = 0.05
    assert mse <= threshold, f"MSE of interpolated temperatures is {mse:.4f}, which exceeds the threshold of {threshold}."