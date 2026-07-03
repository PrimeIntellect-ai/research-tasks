# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_correct():
    """Test that report.json exists and contains the correct values."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Missing report file: {report_path}"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_keys = {"hidden_size", "positive_count", "p_value"}
    assert set(report.keys()) == expected_keys, f"report.json keys mismatch. Expected {expected_keys}, got {set(report.keys())}"

    assert report["hidden_size"] == 8, f"Expected hidden_size to be 8, got {report['hidden_size']}"
    assert report["positive_count"] == 43, f"Expected positive_count to be 43, got {report['positive_count']}"

    # Allow a small float tolerance for p_value, though the prompt says exact rounded to 4 decimals
    assert abs(report["p_value"] - 0.1933) < 1e-4, f"Expected p_value to be ~0.1933, got {report['p_value']}"

def test_model_def_fixed():
    """Test that model_def.py was updated to the correct hidden size."""
    file_path = "/home/user/model_def.py"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    assert "class SimpleMLP" in content, "model_def.py does not contain the SimpleMLP class."
    assert "nn.Linear(3, 8)" in content, "model_def.py does not contain the corrected hidden size (8) for fc1."
    assert "nn.Linear(8, 1)" in content, "model_def.py does not contain the corrected hidden size (8) for fc2."