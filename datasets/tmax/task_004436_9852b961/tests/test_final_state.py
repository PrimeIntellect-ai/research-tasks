# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_output_exists_and_mse_below_threshold():
    output_path = "/home/user/results/state_distribution.csv"
    reference_path = "/tmp/reference_distribution.csv"

    assert os.path.isfile(output_path), f"Output file does not exist at {output_path}"
    assert os.path.isfile(reference_path), f"Reference file does not exist at {reference_path}"

    try:
        df_out = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read output CSV: {e}")

    try:
        df_ref = pd.read_csv(reference_path)
    except Exception as e:
        pytest.fail(f"Failed to read reference CSV: {e}")

    assert "node_id" in df_out.columns, "Output CSV is missing 'node_id' column"
    assert "probability" in df_out.columns, "Output CSV is missing 'probability' column"
    assert "node_id" in df_ref.columns, "Reference CSV is missing 'node_id' column"
    assert "probability" in df_ref.columns, "Reference CSV is missing 'probability' column"

    # Merge on node_id
    df_merged = pd.merge(df_out, df_ref, on="node_id", suffixes=('_out', '_ref'))

    assert len(df_merged) > 0, "No matching node_ids found between output and reference"

    # Calculate MSE
    mse = np.mean((df_merged['probability_out'] - df_merged['probability_ref'])**2)

    threshold = 1e-6
    assert mse <= threshold, f"MSE is {mse}, which is greater than the threshold {threshold}. The integrator logic might still be incorrect."