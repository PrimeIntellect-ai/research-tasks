# test_final_state.py

import os
import json
import pytest

APP_DIR = "/home/user/app"

def test_hasher_compiled():
    hasher_path = os.path.join(APP_DIR, "hasher")
    assert os.path.isfile(hasher_path), f"Compiled executable {hasher_path} does not exist. Ensure you compiled hasher.c."
    assert os.access(hasher_path, os.X_OK), f"File {hasher_path} is not executable."

def test_new_schema_jsonl():
    jsonl_path = os.path.join(APP_DIR, "new_schema.jsonl")
    assert os.path.isfile(jsonl_path), f"Target file {jsonl_path} does not exist. Ensure your script generates it."

    csv_path = os.path.join(APP_DIR, "legacy.csv")
    assert os.path.isfile(csv_path), f"Source file {csv_path} does not exist."

    expected_data = {}
    with open(csv_path, "r") as f:
        lines = f.read().strip().split('\n')
        for line in lines[1:]: # skip header
            if not line.strip(): 
                continue
            user_id, filepath = line.split(',')

            full_filepath = os.path.join(APP_DIR, filepath)
            assert os.path.isfile(full_filepath), f"Expected data file {full_filepath} is missing."

            with open(full_filepath, "rb") as bf:
                content = bf.read()

            # Simulate the C hasher utility: prepends "WEB_"
            modified_content = b"WEB_" + content

            # Simulate the Python checksum logic: sum of first 8 bytes modulo 255
            chunk = modified_content[:8]
            expected_hash = sum(chunk) % 255

            expected_data[str(user_id)] = expected_hash

    actual_data = {}
    with open(jsonl_path, "r") as f:
        for line in f:
            if not line.strip(): 
                continue
            try:
                obj = json.loads(line)
                assert "user_id" in obj, f"Missing 'user_id' in JSON object: {line}"
                assert "avatar_hash" in obj, f"Missing 'avatar_hash' in JSON object: {line}"
                actual_data[str(obj["user_id"])] = obj["avatar_hash"]
            except json.JSONDecodeError as e:
                pytest.fail(f"Could not parse line in {jsonl_path} as JSON: '{line}'. Error: {e}")

    assert actual_data == expected_data, f"Contents of {jsonl_path} do not match the expected computed hashes. Expected: {expected_data}, Actual: {actual_data}"