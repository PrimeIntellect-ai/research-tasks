# test_final_state.py
import os
import pytest

def test_compliance_violations_output():
    output_file = "/home/user/compliance_violations.txt"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    expected_entities = [
        "Alice",
        "App1",
        "App2",
        "Charlie",
        "DataLake",
        "Eve",
        "ServiceA",
        "ServiceB",
        "ServiceC"
    ]

    with open(output_file, "r") as f:
        content = f.read().strip()

    actual_entities = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_entities == expected_entities, (
        f"The contents of {output_file} do not match the expected output.\n"
        f"Expected: {expected_entities}\n"
        f"Actual: {actual_entities}"
    )

def test_cpp_file_exists():
    cpp_file = "/home/user/audit.cpp"
    assert os.path.exists(cpp_file), f"Source file {cpp_file} does not exist."
    assert os.path.isfile(cpp_file), f"{cpp_file} is not a file."