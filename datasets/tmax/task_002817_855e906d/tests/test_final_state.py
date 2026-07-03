# test_final_state.py
import os
import json

def test_api_response_json_exists_and_valid():
    file_path = '/home/user/api_response.json'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} does not contain valid JSON."

    expected_data = [
        {"version": "1.5.0", "data": "start of v1.5"},
        {"version": "1.11.2", "data": "higher minor"},
        {"version": "2.0.1", "data": "major update"}
    ]

    assert data == expected_data, f"The content of {file_path} does not match the expected JSON structure and values."

def test_benchmark_txt_exists_and_non_empty():
    file_path = '/home/user/benchmark.txt'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    assert os.path.getsize(file_path) > 0, f"The file {file_path} is empty."

    with open(file_path, 'r') as f:
        content = f.read().lower()

    # Check for common keywords from benchmarking tools like `time`
    keywords = ['real', 'user', 'sys', 'system', 'cpu', 'seconds']
    assert any(kw in content for kw in keywords), f"The file {file_path} does not appear to contain valid benchmark output."