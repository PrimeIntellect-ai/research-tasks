# test_final_state.py

import os
import json
import subprocess
import pytest

def test_cleaned_logs_parquet_exists():
    parquet_path = '/home/user/artifacts/cleaned_logs.parquet'
    assert os.path.isfile(parquet_path), f"The file {parquet_path} does not exist."

def test_posteriors_json():
    json_path = '/home/user/artifacts/posteriors.json'
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = {
        "model_alpha": {"alpha": 402, "beta": 102},
        "model_beta": {"alpha": 512, "beta": 92}
    }

    assert data == expected_data, f"The contents of {json_path} do not match the expected posterior parameters."

def test_bootstrap_ci_txt():
    txt_path = '/home/user/artifacts/bootstrap_ci.txt'
    assert os.path.isfile(txt_path), f"The file {txt_path} does not exist."

    # Compute the expected CI using a subprocess to adhere to the standard-library-only rule for the test script
    # while utilizing the numpy/pandas installed in the environment.
    script = """
import pandas as pd
import numpy as np

df_alpha = pd.DataFrame({'correct': [1]*400 + [0]*100, 'model': 'model_alpha'})
df_beta = pd.DataFrame({'correct': [1]*510 + [0]*90, 'model': 'model_beta'})
df_clean = pd.concat([df_alpha, df_beta]).reset_index(drop=True)

np.random.seed(123)
diffs = []
n_size = len(df_clean)

for _ in range(10000):
    idx = np.random.choice(n_size, size=n_size, replace=True)
    sample = df_clean.iloc[idx]

    acc_alpha = sample[sample['model'] == 'model_alpha']['correct'].mean()
    acc_beta = sample[sample['model'] == 'model_beta']['correct'].mean()

    if pd.isna(acc_alpha): acc_alpha = 0
    if pd.isna(acc_beta): acc_beta = 0

    diffs.append(acc_beta - acc_alpha)

lower = np.percentile(diffs, 2.5)
upper = np.percentile(diffs, 97.5)

print(f"{lower:.4f},{upper:.4f}")
"""
    try:
        result = subprocess.run(['python3', '-c', script], capture_output=True, text=True, check=True)
        expected_ci = result.stdout.strip()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to compute expected bootstrap CI. Ensure numpy and pandas are installed.")

    with open(txt_path, 'r') as f:
        actual_ci = f.read().strip()

    assert actual_ci == expected_ci, f"The bootstrap CI in {txt_path} ('{actual_ci}') does not match the expected value ('{expected_ci}')."