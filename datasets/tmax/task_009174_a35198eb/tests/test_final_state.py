# test_final_state.py
import os
import json

def test_notebook_exists_and_valid():
    """Check if the Jupyter Notebook exists and is valid JSON."""
    notebook_path = '/home/user/workspace/extract_features.ipynb'
    assert os.path.isfile(notebook_path), f"Notebook missing: {notebook_path}"

    with open(notebook_path, 'r') as f:
        try:
            nb_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Notebook {notebook_path} is not a valid JSON file."

    assert "cells" in nb_data, "Notebook missing 'cells' key, might not be a valid Jupyter Notebook."

def test_features_csv_exists_and_correct():
    """Check if features.csv exists and contains the correct singular values."""
    csv_path = '/home/user/workspace/features.csv'
    assert os.path.isfile(csv_path), f"Features file missing: {csv_path}"

    with open(csv_path, 'r') as f:
        content = f.read().strip()

    expected_content = "3.0000,3.0000,1.0000,1.0000,1.0000"

    assert content == expected_content, f"Expected features.csv to contain '{expected_content}', but found '{content}'"