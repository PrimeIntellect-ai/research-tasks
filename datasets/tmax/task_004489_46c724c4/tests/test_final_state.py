# test_final_state.py

import os
import json
import pytest

def test_bug_commit_txt():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bug_commit.txt"

    assert os.path.exists(expected_file), f"Expected bad commit file {expected_file} is missing."
    assert os.path.exists(actual_file), f"User output file {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert expected_hash == actual_hash, f"Expected commit hash '{expected_hash}', but got '{actual_hash}' in {actual_file}."

def test_fixed_output_json():
    output_file = "/home/user/fixed_output.json"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    expected_data = [
        {
            "total_name": "Widget",
            "total_price": 139.5
        },
        {
            "total_name": "Gadget",
            "total_price": 199.5
        }
    ]

    assert data == expected_data, f"The contents of {output_file} do not match the expected calculations."

def test_processor_go_fixed():
    processor_file = "/home/user/app/processor.go"
    assert os.path.exists(processor_file), f"File {processor_file} is missing."

    with open(processor_file, "r") as f:
        content = f.read()

    assert "(1.0 - i.Discount)" in content, "The bug was not fixed correctly in processor.go. Expected to find '(1.0 - i.Discount)'."
    assert "(1.0 + i.Discount)" not in content, "The bug is still present in processor.go. Found '(1.0 + i.Discount)'."