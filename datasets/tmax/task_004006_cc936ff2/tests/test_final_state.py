# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    """Test that the python script process_math.py exists."""
    script_path = '/home/user/process_math.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_json_output_exists():
    """Test that the output JSON file exists."""
    json_path = '/home/user/extracted_math.json'
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

def test_json_output_content():
    """Test that the output JSON file contains the correct extracted and evaluated math data."""
    json_path = '/home/user/extracted_math.json'
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected = {
        "doc1.txt": {"trace": 7, "poly_eval_10": 229},
        "doc2.dat": {"trace": 2, "poly_eval_10": 90},
        "doc3.log": {"trace": 11, "poly_eval_10": 43}
    }

    assert isinstance(data, dict), "The JSON root should be a dictionary."

    for doc, expected_values in expected.items():
        assert doc in data, f"Missing key '{doc}' in the JSON output."
        assert "trace" in data[doc], f"Missing 'trace' for '{doc}'."
        assert "poly_eval_10" in data[doc], f"Missing 'poly_eval_10' for '{doc}'."

        assert data[doc]["trace"] == expected_values["trace"], \
            f"Incorrect trace for '{doc}'. Expected {expected_values['trace']}, got {data[doc]['trace']}."
        assert data[doc]["poly_eval_10"] == expected_values["poly_eval_10"], \
            f"Incorrect poly_eval_10 for '{doc}'. Expected {expected_values['poly_eval_10']}, got {data[doc]['poly_eval_10']}."

    # Check for unexpected extra keys
    extra_keys = set(data.keys()) - set(expected.keys())
    assert not extra_keys, f"Unexpected extra keys in JSON output: {extra_keys}"