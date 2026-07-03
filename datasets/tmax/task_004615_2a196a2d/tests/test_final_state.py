# test_final_state.py

import os
import json
import pytest

def test_parser_executable_exists():
    path = "/home/user/parser"
    assert os.path.isfile(path), f"Missing compiled executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_analyze_py_updated():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, 'r') as f:
        content = f.read()
    assert "parser" in content, "The script /home/user/analyze.py does not seem to call the 'parser' executable."
    assert "np.fromfile" in content or "fromfile" in content or "open" in content, "The script does not seem to read the binary file."

def test_result_json_exists_and_correct():
    path = "/home/user/result.json"
    assert os.path.isfile(path), f"Missing result file: {path}"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "peak_index" in data, "Missing key 'peak_index' in result.json"
    assert "peak_magnitude" in data, "Missing key 'peak_magnitude' in result.json"

    assert data["peak_index"] == 25000, f"Expected peak_index to be 25000, got {data['peak_index']}"
    assert abs(data["peak_magnitude"] - 70710.7) < 0.1, f"Expected peak_magnitude to be 70710.7, got {data['peak_magnitude']}"