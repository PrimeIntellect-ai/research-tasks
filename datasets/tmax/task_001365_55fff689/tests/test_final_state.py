# test_final_state.py
import os
import re

def test_results_file_exists():
    file_path = "/home/user/results.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing. Did you run the script?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_results_content():
    file_path = "/home/user/results.txt"
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, found {len(lines)}."

    records_match = re.match(r"^Total Records:\s*(\d+)$", lines[0])
    assert records_match, f"First line format is incorrect. Expected 'Total Records: <integer>', got '{lines[0]}'"
    records = int(records_match.group(1))
    assert records == 10000, f"Expected 10000 Total Records, got {records}. Concurrency or retry logic might still be broken."

    value_match = re.match(r"^Total Value:\s*([0-9\.]+)$", lines[1])
    assert value_match, f"Second line format is incorrect. Expected 'Total Value: <precise string>', got '{lines[1]}'"
    value_str = value_match.group(1)

    # Check for exact floating point text representation of Decimal('1000.0')
    # Depending on how the user initialized Decimal, it might be '1000.0'
    # It should not be '1000.0000000000001' or similar floating point artifacts.
    assert value_str == "1000.0", f"Expected Total Value to be exactly '1000.0' using Decimal, got '{value_str}'. Floating-point precision issue might not be properly fixed."