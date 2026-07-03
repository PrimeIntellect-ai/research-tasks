# test_final_state.py

import os
import json
import tomli # Using built-in tomllib in Python 3.11+, but since we can't guarantee 3.11+, we can check if it parses or just check the contents.
import sys

def test_pyproject_toml_fixed():
    """Test that pyproject.toml is fixed and contains Flask dependency."""
    file_path = '/home/user/qa_env/pyproject.toml'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    # Check that Flask is in dependencies
    assert 'Flask' in content or 'flask' in content, "pyproject.toml is missing the Flask dependency."

    # Check that the syntax error is fixed
    # We can try to parse it using tomllib if available
    if sys.version_info >= (3, 11):
        import tomllib
        try:
            with open(file_path, 'rb') as f:
                tomllib.load(f)
        except Exception as e:
            assert False, f"pyproject.toml still has a syntax error: {e}"

def test_result_json_correct():
    """Test that test_result.json contains the correct expected output."""
    file_path = '/home/user/qa_env/test_result.json'
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run the curl command and save the output?"

    with open(file_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    assert 'checksum' in result, "Result JSON is missing 'checksum' field."
    assert 'data' in result, "Result JSON is missing 'data' field."

    assert result['checksum'] == 3776263595, f"Expected checksum 3776263595, got {result['checksum']}."

    data = result['data']
    assert data.get('id') == 892, f"Expected data.id to be 892, got {data.get('id')}."
    assert data.get('name') == "Charlie", f"Expected data.name to be 'Charlie', got {data.get('name')}."
    assert data.get('balance_dollars') == 42.5, f"Expected data.balance_dollars to be 42.5, got {data.get('balance_dollars')}."