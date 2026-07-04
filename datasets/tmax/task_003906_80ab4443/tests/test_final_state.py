# test_final_state.py

import os
import json
import pytest

def test_venv_exists():
    venv_python = '/home/user/venv/bin/python'
    assert os.path.isfile(venv_python), f"Virtual environment python executable not found at {venv_python}. Did you create the venv?"

def test_metrics_json_exists_and_valid():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"File not found: {metrics_path}. Did you run the pipeline successfully?"

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} does not contain valid JSON.")

    assert 'accuracy' in data, f"'accuracy' key missing in {metrics_path}"

    acc = data['accuracy']
    assert isinstance(acc, float), f"'accuracy' should be a float, got {type(acc)}"
    assert 0.0 <= acc <= 1.0, f"'accuracy' value out of expected bounds [0.0, 1.0]: {acc}"

def test_etl_pipeline_modified():
    pipeline_path = '/home/user/etl_pipeline.py'
    assert os.path.isfile(pipeline_path), f"File not found: {pipeline_path}"

    with open(pipeline_path, 'r') as f:
        content = f.read()

    # Check for some form of dropping NaNs or filtering
    has_drop = 'dropna' in content or 'notnull' in content or 'how=\'inner\'' in content or 'how="inner"' in content or 'inner' in content
    assert has_drop, "The ETL script does not seem to contain logic to drop missing values (e.g., dropna or inner join)."

    # Check for casting to int
    has_cast = 'astype(int)' in content or 'astype("int")' in content or "astype('int')" in content or "astype('int64')" in content or 'astype("int64")' in content or 'to_numeric' in content
    assert has_cast or has_drop, "The ETL script does not seem to contain logic to handle the missing values and fix the data type."