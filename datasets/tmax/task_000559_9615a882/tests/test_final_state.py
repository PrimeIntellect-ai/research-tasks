# test_final_state.py

import os
import pandas as pd
import pytest

def test_dataset_exists():
    """Verify that the dataset file was generated."""
    path = '/home/user/dataset.csv'
    assert os.path.isfile(path), f"Dataset file {path} was not generated. Did you run the simulator?"

def test_energy_conservation():
    """Verify that the maximum relative energy drift is within the acceptable threshold."""
    path = '/home/user/dataset.csv'
    assert os.path.isfile(path), f"Dataset file {path} is missing."

    # Read the dataset
    try:
        df = pd.read_csv(path)
    except Exception as e:
        pytest.fail(f"Failed to read {path} as a CSV file: {e}")

    # Check for the required 'E' column
    assert 'E' in df.columns, "Column 'E' (total energy) not found in dataset.csv."

    # Ensure there's data
    assert len(df) > 0, "The dataset is empty."

    # Calculate the maximum relative energy drift
    e0 = df['E'].iloc[0]
    assert e0 != 0, "Initial energy E_0 is exactly zero, which prevents calculating relative drift."

    relative_drifts = (df['E'] - e0).abs() / abs(e0)
    max_drift = relative_drifts.max()

    threshold = 1e-3
    assert max_drift <= threshold, (
        f"Maximum relative energy drift is {max_drift:.6e}, which exceeds the strict "
        f"threshold of {threshold}. The RK45 error estimation bug might not be fully fixed."
    )