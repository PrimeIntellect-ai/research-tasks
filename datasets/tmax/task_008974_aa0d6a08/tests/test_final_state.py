# test_final_state.py
import os

def test_means_file_exists_and_content():
    """
    Validates that the output file /home/user/means.txt was created and 
    contains the correct deterministic bootstrap means.
    """
    output_file = "/home/user/means.txt"
    assert os.path.exists(output_file), f"{output_file} does not exist. Did you run the Rust program?"
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    with open(output_file, 'r') as f:
        lines = f.read().strip().splitlines()

    expected_lines = [
        "29.00",
        "32.00",
        "40.00"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} in {output_file} is incorrect. Expected '{expected}', got '{actual.strip()}'."