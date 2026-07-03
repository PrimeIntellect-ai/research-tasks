# test_final_state.py
import os
import json

def test_script_exists_and_executable():
    script_path = "/home/user/process_logs.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_dashboard_data_exists():
    data_path = "/home/user/dashboard_data.json"
    assert os.path.isfile(data_path), f"Output file missing: {data_path}"

def test_dashboard_data_content():
    data_path = "/home/user/dashboard_data.json"

    with open(data_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Output file {data_path} is not valid JSON"

    assert isinstance(data, list), f"Expected the root of {data_path} to be a JSON array, got {type(data).__name__}"

    expected_data = [
        {
            "error_code": "E0382",
            "file": "src/main.rs",
            "line": 5
        },
        {
            "error_code": "E0382",
            "file": "src/config.rs",
            "line": 42
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} elements in the JSON array, but found {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}:\nExpected: {expected}\nActual: {actual}"