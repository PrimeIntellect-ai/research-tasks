# test_final_state.py

import os
import json
import pytest

def test_c_program_exists():
    """Test that the C program source file was created."""
    file_path = '/home/user/analyze.c'
    assert os.path.isfile(file_path), f"Missing required C program file: {file_path}"

def test_analysis_result_exists():
    """Test that the output JSON file exists."""
    file_path = '/home/user/analysis_result.json'
    assert os.path.isfile(file_path), f"Missing required output file: {file_path}"

def test_analysis_result_json_content():
    """Test that the JSON file contains the correct parsed values."""
    file_path = '/home/user/analysis_result.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert "feature" in data, "Missing 'feature' key in JSON output."
    assert "threshold" in data, "Missing 'threshold' key in JSON output."
    assert "accuracy" in data, "Missing 'accuracy' key in JSON output."

    assert data["feature"] == "pressure_feature", f"Expected feature 'pressure_feature', got '{data['feature']}'"
    assert data["threshold"] == 73, f"Expected threshold 73, got {data['threshold']}"
    assert pytest.approx(data["accuracy"], abs=0.001) == 0.916, f"Expected accuracy ~0.916, got {data['accuracy']}"

def test_analysis_result_exact_formatting():
    """Test that the JSON file matches the exact requested formatting and spacing."""
    file_path = '/home/user/analysis_result.json'

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_content = '{\n  "feature": "pressure_feature",\n  "threshold": 73,\n  "accuracy": 0.916\n}'

    # Normalize line endings to prevent failures due to CRLF vs LF
    content = content.replace('\r\n', '\n')

    assert content == expected_content, (
        f"The JSON formatting does not exactly match the requested output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )