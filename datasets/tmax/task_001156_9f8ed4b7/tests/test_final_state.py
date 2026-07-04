# test_final_state.py

import os
import json
import pytest

def test_result_json_exists():
    """Test that result.json has been created."""
    assert os.path.isfile("/home/user/result.json"), "/home/user/result.json does not exist. Did you execute process.py?"

def test_result_json_content():
    """Test that result.json contains the correct filtered IDs."""
    with open("/home/user/result.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/result.json is not a valid JSON file.")

    assert isinstance(results, list), "/home/user/result.json must contain a JSON array."
    assert results == [101, 103], f"Expected IDs [101, 103], but got {results}. Check your decoding logic and ctypes ABI definitions."

def test_data_json_unmodified():
    """Test that data.json was not modified."""
    assert os.path.isfile("/home/user/data.json"), "/home/user/data.json is missing."
    with open("/home/user/data.json", "r") as f:
        content = f.read()
    assert "QQBQAEkAXwBWAEEATABJAEQAXwBUAEUAUwBUAA==" in content, "data.json was modified."
    assert "SQBOAFYAQQBMAEkARABfAEQAQQBUAEEA" in content, "data.json was modified."