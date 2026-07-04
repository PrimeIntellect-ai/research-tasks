# test_final_state.py
import os
import json
import subprocess
import pytest

def test_importance_png_exists():
    path = '/home/user/importance.png'
    assert os.path.isfile(path), f"File {path} does not exist. The plot was not saved correctly."
    assert os.path.getsize(path) > 0, f"File {path} is empty."

    # Check if it's a valid PNG file by reading the magic number
    with open(path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"File {path} is not a valid PNG image."

def test_metrics_json():
    path = '/home/user/metrics.json'
    assert os.path.isfile(path), f"File {path} does not exist. Metrics were not saved."

    with open(path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "accuracy" in metrics, "Key 'accuracy' missing in metrics.json"
    assert "f1_score" in metrics, "Key 'f1_score' missing in metrics.json"

    assert isinstance(metrics["accuracy"], (int, float)), "'accuracy' must be a numeric value"
    assert isinstance(metrics["f1_score"], (int, float)), "'f1_score' must be a numeric value"

def test_pipeline_headless_config():
    path = '/home/user/pipeline.py'
    assert os.path.isfile(path), f"File {path} missing."

    with open(path, 'r') as f:
        content = f.read()

    assert 'savefig' in content, "plt.savefig is not used in pipeline.py"
    # It shouldn't have plt.show() or it should have Agg
    # We will just check that savefig is used and it doesn't crash (which is implied by PNG existing).

def test_pytest_execution():
    test_file = '/home/user/test_pipeline.py'
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    result = subprocess.run(['pytest', test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest {test_file} failed with output:\n{result.stdout}\n{result.stderr}"
    assert 'test_clean_data' in result.stdout or 'test_clean_data' in open(test_file).read(), "test_clean_data not found in test file or execution."