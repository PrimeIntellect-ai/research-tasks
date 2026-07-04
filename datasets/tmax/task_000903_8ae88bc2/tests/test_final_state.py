# test_final_state.py

import os
import json
import pytest

def test_error_archive_exists_and_valid():
    output_path = '/home/user/error_archive.json'

    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

    with open(output_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {output_path} does not contain valid JSON: {e}")

    assert isinstance(data, list), "The JSON output must be an array (list) of objects."
    assert len(data) == 2, f"Expected exactly 2 ERROR records, but found {len(data)}."

    # Check first record
    assert data[0].get("TIMESTAMP") == "2023-10-25T10:01:00Z", "First record TIMESTAMP mismatch."
    assert data[0].get("LEVEL") == "ERROR", "First record LEVEL mismatch."
    assert data[0].get("MSG") == "Volume shadow copy failed", "First record MSG mismatch."
    assert data[0].get("DETAILS") == "VSS writer error 0x8004231f", "First record DETAILS mismatch."

    # Check second record
    assert data[1].get("TIMESTAMP") == "2023-10-25T10:05:00Z", "Second record TIMESTAMP mismatch."
    assert data[1].get("LEVEL") == "ERROR", "Second record LEVEL mismatch."
    assert data[1].get("MSG") == "Network timeout", "Second record MSG mismatch."
    assert data[1].get("DETAILS") == "Destination unreachable after 30s", "Second record DETAILS mismatch."

    # Ensure no extra keys are present and no [RECORD] markers
    for record in data:
        for key, value in record.items():
            assert "[RECORD]" not in key and "[/RECORD]" not in key, f"Marker found in key: {key}"
            assert "[RECORD]" not in str(value) and "[/RECORD]" not in str(value), f"Marker found in value: {value}"