# test_final_state.py

import os
import json
import pytest

def test_plot_generated():
    plot_path = '/home/user/data/plot.png'
    assert os.path.isfile(plot_path), f"Plot file {plot_path} was not generated."

    # A blank plot saved after plt.show() is typically very small.
    # A plot with actual data should be larger than 2000 bytes.
    file_size = os.path.getsize(plot_path)
    assert file_size > 2000, f"Plot file {plot_path} is too small ({file_size} bytes), indicating it might still be blank."

def test_parquet_generated():
    parquet_path = '/home/user/data/features.parquet'
    assert os.path.isfile(parquet_path), f"Parquet file {parquet_path} was not generated."

    with open(parquet_path, 'rb') as f:
        header = f.read(4)
        f.seek(-4, os.SEEK_END)
        footer = f.read(4)

    assert header == b'PAR1', f"{parquet_path} does not have a valid Parquet header."
    assert footer == b'PAR1', f"{parquet_path} does not have a valid Parquet footer."

    # Heuristic check for column names in the binary file since we can't use pandas/pyarrow
    with open(parquet_path, 'rb') as f:
        content = f.read()

    assert b'id' in content, "Column 'id' not found in the Parquet file metadata."
    assert b'feature_vector' in content, "Column 'feature_vector' not found in the Parquet file metadata."

def test_recommendations_json():
    json_path = '/home/user/recommendations.json'
    assert os.path.isfile(json_path), f"Recommendations JSON file {json_path} was not generated."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_data = {"target": 101, "similar": [103, 105]}
    assert data == expected_data, f"Recommendations JSON content is incorrect. Expected {expected_data}, got {data}."