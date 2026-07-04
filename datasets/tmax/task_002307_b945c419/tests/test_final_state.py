# test_final_state.py
import os
import json

def test_normalized_configs_exists_and_valid():
    file_path = '/home/user/normalized_configs.json'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} does not contain valid JSON."

    assert isinstance(data, list), f"The data in {file_path} must be a JSON array."
    assert len(data) == 3, f"Expected 3 records in {file_path}, found {len(data)}."

    expected_data = [
        {"server": "srv-01", "timestamp": "2023-10-01T14:00:00Z", "key": "max_conns", "value": "100"},
        {"server": "srv-02", "timestamp": "2023-10-01T14:05:00Z", "key": "timeout", "value": "30s"},
        {"server": "srv-03", "timestamp": "2023-10-02T10:00:00Z", "key": "retries", "value": "3"}
    ]

    assert data == expected_data, f"The data in {file_path} does not match the expected normalized, deduplicated, and sorted output."

def test_pipeline_log_exists_and_valid():
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, 'r') as f:
        log_contents = f.read().strip()

    expected_log = "[INFO] Processed 6 raw records. Exported 3 unique records."
    assert expected_log in log_contents, f"The file {log_path} does not contain the expected log message. Found: {log_contents}"