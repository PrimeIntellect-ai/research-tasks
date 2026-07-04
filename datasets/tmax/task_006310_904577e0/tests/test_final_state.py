# test_final_state.py

import os
import re
import base64
import pytest

def test_payload_script_exists():
    path = "/home/user/payload.py"
    assert os.path.isfile(path), f"The payload script {path} was not found. You must create it to complete the task."

def test_extracted_command_file_exists():
    path = "/home/user/extracted_command.txt"
    assert os.path.isfile(path), f"The output file {path} was not found. Your payload must create this file."

def test_extracted_command_content():
    c2_server_path = "/home/user/c2_server.py"
    output_path = "/home/user/extracted_command.txt"

    assert os.path.isfile(c2_server_path), f"The C2 server script {c2_server_path} is missing, cannot verify truth data."
    assert os.path.isfile(output_path), f"The output file {output_path} is missing."

    # Derive the expected truth by parsing the C2 server script
    with open(c2_server_path, 'r') as f:
        c2_content = f.read()

    match = re.search(r'C2-Session-Token=([A-Za-z0-9+/=]+)', c2_content)
    assert match is not None, "Could not find the Base64 session token in the C2 server script to derive the expected command."

    base64_token = match.group(1)
    try:
        expected_command = base64.b64decode(base64_token).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decode the expected Base64 token from the C2 server: {e}")

    # Read the student's output
    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert expected_command in actual_output, (
        f"The file {output_path} does not contain the correct decoded command. "
        f"Expected to find '{expected_command}', but got '{actual_output}'."
    )