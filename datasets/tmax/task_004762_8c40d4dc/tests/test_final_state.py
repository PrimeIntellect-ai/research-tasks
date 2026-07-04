# test_final_state.py

import os
import pandas as pd
import pytest

def test_etl_pipeline_script_exists():
    script_path = '/home/user/etl_pipeline.sh'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_results_csv_exists():
    results_path = '/home/user/results.csv'
    assert os.path.exists(results_path), f"The output file {results_path} does not exist."
    assert os.path.isfile(results_path), f"The path {results_path} is not a file."

def test_results_csv_metric():
    results_path = '/home/user/results.csv'
    assert os.path.exists(results_path), f"The output file {results_path} does not exist."

    try:
        pred_df = pd.read_csv(results_path)
    except Exception as e:
        pytest.fail(f"Failed to read {results_path} as a CSV: {e}")

    # Check columns
    expected_columns = ['ID', 'Score']
    actual_columns = list(pred_df.columns)
    assert actual_columns == expected_columns, f"Expected columns {expected_columns}, but got {actual_columns}."

    # True data derived from the prompt
    true_data = {
        1: 8.25,
        2: 16.525,
        3: 6.0,
        4: 25.225,
        5: 12.25
    }

    # Verify all IDs are present and sorted
    ids = pred_df['ID'].astype(int).tolist()
    assert ids == [1, 2, 3, 4, 5], f"Expected IDs [1, 2, 3, 4, 5] in order, but got {ids}."

    # Compute MSE
    mse = 0.0
    for _, row in pred_df.iterrows():
        i = int(row['ID'])
        if i in true_data:
            try:
                score = float(row['Score'])
            except ValueError:
                pytest.fail(f"Score for ID {i} is not a valid float: {row['Score']}")
            mse += (score - true_data[i]) ** 2
        else:
            pytest.fail(f"Unexpected ID {i} found in {results_path}.")

    mse = mse / len(true_data)

    # Assert metric threshold
    threshold = 0.05
    assert mse <= threshold, f"Calculated MSE {mse} exceeds the allowed threshold of {threshold}."