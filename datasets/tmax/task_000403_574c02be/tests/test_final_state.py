# test_final_state.py

import os
import pytest

def test_cleaned_data_exists():
    assert os.path.isfile('/home/user/data/cleaned_data.csv'), "/home/user/data/cleaned_data.csv is missing. Did you run clean_pipeline.py?"

def test_cleaned_data_no_floats():
    with open('/home/user/data/cleaned_data.csv', 'r') as f:
        content = f.read()

    # The requirement is that quality_label should not contain floats like `.0`.
    assert ".0" not in content, "Found '.0' in cleaned_data.csv. The quality_label column was likely cast to float instead of Int64."

    # Check that the last row has an empty value for quality_label
    lines = content.strip().split('\n')
    assert len(lines) >= 6, "cleaned_data.csv does not have the expected number of rows."

    # Row 105 should end with a comma (no value) or we check specific lines
    # Data: 101,1; 102,0; 103,0; 104,1; 105,
    assert lines[1].endswith(",1") or lines[1].endswith(",1\r"), "Row 101 should end with 1"
    assert lines[2].endswith(",0") or lines[2].endswith(",0\r"), "Row 102 should end with 0"
    assert lines[-1].endswith(",") or lines[-1].endswith(",\r"), "Row 105 should have an empty quality_label"

def test_predict_script_exists():
    assert os.path.isfile('/home/user/predict.py'), "/home/user/predict.py is missing. Did you write the prediction script?"

def test_prediction_output():
    assert os.path.isfile('/home/user/data/prediction.txt'), "/home/user/data/prediction.txt is missing. Did you save the prediction?"

    with open('/home/user/data/prediction.txt', 'r') as f:
        pred = f.read().strip()

    assert pred == "0", f"Expected prediction to be '0', but got '{pred}'"