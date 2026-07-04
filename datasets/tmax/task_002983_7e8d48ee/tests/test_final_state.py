# test_final_state.py

import os
import json

def test_output_json_exists_and_valid():
    """Verify that output.json exists and is a valid JSON array with exactly 20 elements."""
    output_file = "/home/user/log_processor/output.json"

    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run app.py successfully?"

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_file} does not contain valid JSON."

    assert isinstance(data, list), f"Expected {output_file} to contain a JSON array."
    assert len(data) == 20, f"Expected exactly 20 elements in {output_file}, but found {len(data)}."

    # Check that the edge case was handled correctly
    edge_case_found = False
    for entry in data:
        if entry.get("message") == 'Failed to parse user input "admin" from payload':
            edge_case_found = True
            break

    assert edge_case_found, "The edge case message with double quotes was not found or not parsed correctly in output.json."

def test_resolution_txt_correct():
    """Verify that resolution.txt exists and contains the correct information."""
    resolution_file = "/home/user/resolution.txt"

    assert os.path.isfile(resolution_file), f"Resolution file {resolution_file} is missing."

    with open(resolution_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {resolution_file}, but found {len(lines)}."

    assert lines[0] == "server_07.log", f"Expected the first line of {resolution_file} to be 'server_07.log', but got '{lines[0]}'."
    assert lines[1] == "SUCCESS", f"Expected the second line of {resolution_file} to be 'SUCCESS', but got '{lines[1]}'."