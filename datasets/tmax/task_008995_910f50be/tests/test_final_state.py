# test_final_state.py
import os
import json
import pytest

def test_chunk_1_exists_and_content():
    path = "/home/user/processed/chunk_1.json"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_data = [
        {"hostname": "srv1", "used_gb": 85},
        {"hostname": "srv3", "used_gb": 190}
    ]

    assert data == expected_data, f"Content of {path} does not match expected output. Got: {data}"

def test_chunk_2_exists_and_content():
    path = "/home/user/processed/chunk_2.json"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_data = [
        {"hostname": "srv4", "used_gb": 450},
        {"hostname": "srv6", "used_gb": 90}
    ]

    assert data == expected_data, f"Content of {path} does not match expected output. Got: {data}"

def test_chunk_3_does_not_exist():
    path = "/home/user/processed/chunk_3.json"
    assert not os.path.exists(path), f"File {path} should not exist."

def test_watcher_go_exists():
    path = "/home/user/watcher.go"
    assert os.path.isfile(path), f"Expected Go source file {path} does not exist."