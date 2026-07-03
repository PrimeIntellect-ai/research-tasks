# test_final_state.py

import os
import json
import pytest

def test_metrics_json():
    metrics_path = '/home/user/output/metrics.json'
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist. Did you run the pipeline and output the metrics?"

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} is not a valid JSON file.")

    assert "missing_dropped" in data, "metrics.json is missing the 'missing_dropped' key."
    assert "outliers_dropped" in data, "metrics.json is missing the 'outliers_dropped' key."
    assert "valid_records" in data, "metrics.json is missing the 'valid_records' key."

    assert data["missing_dropped"] == 1, f"Expected 1 missing_dropped, got {data['missing_dropped']}"
    assert data["outliers_dropped"] == 1, f"Expected 1 outliers_dropped, got {data['outliers_dropped']}"
    assert data["valid_records"] == 3, f"Expected 3 valid_records, got {data['valid_records']}"

def test_scatter_png():
    img_path = '/home/user/output/scatter.png'
    assert os.path.exists(img_path), f"{img_path} does not exist. Did you generate the scatter plot?"

    size = os.path.getsize(img_path)
    assert size > 3000, f"{img_path} is too small ({size} bytes). It appears to be blank or corrupted. Ensure the drawing context is properly handled."