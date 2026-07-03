# test_final_state.py

import os
import json
import re
import hashlib

def test_unique_configs_json_exists_and_correct():
    log_file = "/home/user/config_changes.log"
    json_file = "/home/user/unique_configs.json"

    assert os.path.exists(log_file), f"The log file {log_file} is missing. Setup might have been corrupted."
    assert os.path.exists(json_file), f"The output file {json_file} was not created."

    # Derive expected output dynamically from the log file
    expected_counts = {}
    with open(log_file, "r") as f:
        for line in f:
            match = re.search(r"PAYLOAD=\{(.*?)\}", line)
            if match:
                payload = match.group(1)
                sha256_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
                expected_counts[sha256_hash] = expected_counts.get(sha256_hash, 0) + 1

    # Read the actual output
    with open(json_file, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            raise AssertionError(f"The file {json_file} does not contain valid JSON.")

    # Assert exact match
    assert actual_data == expected_counts, (
        f"The contents of {json_file} do not match the expected counts.\n"
        f"Expected: {expected_counts}\n"
        f"Actual: {actual_data}"
    )