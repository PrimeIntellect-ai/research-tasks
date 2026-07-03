# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"ETL script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"ETL script at {script_path} is not executable"

def test_final_csv_exists():
    final_csv_path = "/home/user/final.csv"
    assert os.path.isfile(final_csv_path), f"Final output file missing at {final_csv_path}"
    assert os.path.getsize(final_csv_path) > 0, f"Final output file at {final_csv_path} is empty"

def test_final_csv_encoding_and_mse():
    final_csv_path = "/home/user/final.csv"
    reference_csv_path = "/tmp/reference.csv"

    assert os.path.isfile(reference_csv_path), f"Reference file missing at {reference_csv_path}"

    try:
        # Check UTF-8 encoding by attempting to read with utf-8
        df_final = pd.read_csv(final_csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        pytest.fail(f"The file {final_csv_path} is not valid UTF-8 encoded.")
    except Exception as e:
        pytest.fail(f"Failed to read {final_csv_path}: {e}")

    try:
        df_ref = pd.read_csv(reference_csv_path, encoding='utf-8')
    except Exception as e:
        pytest.fail(f"Failed to read {reference_csv_path}: {e}")

    assert 'value' in df_final.columns, "Column 'value' is missing in the final CSV"
    assert 'value' in df_ref.columns, "Column 'value' is missing in the reference CSV"

    assert len(df_final) == len(df_ref), f"Row count mismatch: final has {len(df_final)} rows, reference has {len(df_ref)} rows."

    # Calculate MSE
    mse = np.mean((df_final['value'] - df_ref['value']) ** 2)
    threshold = 0.1

    assert mse <= threshold, f"MSE is too high: {mse:.4f} > {threshold}. The gap-filling tool might not be using linear interpolation."

def test_no_negative_values():
    final_csv_path = "/home/user/final.csv"
    if not os.path.isfile(final_csv_path):
        pytest.skip("Final CSV not found")

    df_final = pd.read_csv(final_csv_path, encoding='utf-8')
    if 'value' in df_final.columns:
        negative_count = (df_final['value'] < 0).sum()
        assert negative_count == 0, f"Found {negative_count} negative values in the final CSV, which is not allowed."