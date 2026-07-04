# test_final_state.py

import os
import json
import pytest

def test_rotation_result_file():
    """Verify that the rotation_result.json file exists and contains the correct response."""
    result_path = '/home/user/rotation_result.json'

    assert os.path.isfile(result_path), f"The file {result_path} does not exist. Did you save the server response?"

    with open(result_path, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"The file {result_path} does not contain valid JSON. Content: {content}")

    expected_data = {"status": "success", "new_credential": "FLAG_ROTATED_99321"}

    assert data == expected_data, f"The JSON content in {result_path} does not match the expected server response. Found: {data}"