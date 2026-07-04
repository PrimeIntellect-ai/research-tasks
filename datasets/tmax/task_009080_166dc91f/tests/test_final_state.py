# test_final_state.py

import os
import re
import pytest

def test_merged_timeline_exists_and_format():
    file_path = "/home/user/merged_timeline.log"
    assert os.path.isfile(file_path), f"Merged timeline log is missing: {file_path}"

    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) > 0, "Merged timeline log is empty"

    previous_timestamp = -1
    service_a_found = False
    service_b_found = False

    pattern = re.compile(r"^(\d+)\s+\[(SERVICE_A|SERVICE_B)\]\s+(.*)$")

    for line in lines:
        match = pattern.match(line)
        assert match, f"Line does not match required format '<epoch> [SERVICE_NAME] <message>': {line}"

        timestamp = int(match.group(1))
        service_name = match.group(2)
        message = match.group(3)

        # Check chronological sorting
        assert timestamp >= previous_timestamp, f"Timestamps are not sorted chronologically at line: {line}"
        previous_timestamp = timestamp

        if service_name == "SERVICE_A":
            service_a_found = True
            assert not re.match(r"^\d{4}-\d{2}-\d{2}", message), f"Original timestamp was not removed from message: {message}"
        elif service_name == "SERVICE_B":
            service_b_found = True
            assert not re.match(r"^\d+$", message.split(" - ")[0]), f"Original timestamp was not removed from message: {message}"

    assert service_a_found, "No SERVICE_A logs found in the merged timeline"
    assert service_b_found, "No SERVICE_B logs found in the merged timeline"

def test_corrupted_ids_correct():
    file_path = "/home/user/corrupted_ids.txt"
    assert os.path.isfile(file_path), f"Corrupted IDs file is missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, "Corrupted IDs file is empty"

    ids = [line.strip() for line in content.split("\n") if line.strip()]

    # Based on the raw_data.csv, IDs 3 (15.5), 5 (-50), and 7 (50a) have invalid values.
    expected_ids = ["3", "5", "7"]

    assert ids == expected_ids, f"Corrupted IDs do not match the expected sorted list. Expected {expected_ids}, got {ids}"

def test_final_output_correct():
    file_path = "/home/user/app/final_output.txt"
    assert os.path.isfile(file_path), f"Final output file is missing: {file_path}. Did you run the pipeline?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The sum of valid positive integers: 100 + 200 + 300 + 400 + 500 = 1500
    expected_output = "Final Total: 1500"
    assert expected_output in content, f"Final output is incorrect. Expected '{expected_output}', found '{content}'"

def test_service_a_fixed():
    file_path = "/home/user/app/service_a.sh"
    assert os.path.isfile(file_path), f"Service A script is missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read()

    # Ensure the buggy validation was changed
    assert "== *[a-zA-Z]*" not in content, "The buggy validation logic in service_a.sh is still present."