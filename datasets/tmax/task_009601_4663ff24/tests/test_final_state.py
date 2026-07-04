# test_final_state.py

import os
import hashlib
import pytest

def test_cracker_cpp_exists():
    """Check if the student created the cracker.cpp source file."""
    file_path = "/home/user/vuln_scan/cracker.cpp"
    assert os.path.exists(file_path), f"Source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_cracked_txt_exists():
    """Check if the output file cracked.txt was generated."""
    file_path = "/home/user/vuln_scan/cracked.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_cracked_txt_contents():
    """Validate that cracked.txt contains the correct hash:PIN mappings in the correct order."""
    hashes_file = "/home/user/vuln_scan/hashes.txt"
    cracked_file = "/home/user/vuln_scan/cracked.txt"

    assert os.path.exists(hashes_file), f"{hashes_file} is missing."
    assert os.path.exists(cracked_file), f"{cracked_file} is missing."

    with open(hashes_file, 'r') as f:
        original_hashes = f.read().splitlines()

    with open(cracked_file, 'r') as f:
        cracked_lines = f.read().splitlines()

    assert len(cracked_lines) == len(original_hashes), f"Expected {len(original_hashes)} lines in {cracked_file}, but found {len(cracked_lines)}."

    salt = "H4rdC0d3d_S@1t!"
    expected_pins = ["0451", "1337", "4920", "8080", "9999"]

    # Derive the expected mappings
    expected_mappings = []
    for pin in expected_pins:
        target_str = salt + pin
        h = hashlib.sha256(target_str.encode('utf-8')).hexdigest()
        expected_mappings.append(f"{h}:{pin}")

    # Check that the cracked lines match the expected mappings exactly (including order)
    for i, (expected, actual) in enumerate(zip(expected_mappings, cracked_lines)):
        assert actual == expected, f"Line {i+1} in {cracked_file} is incorrect. Expected '{expected}', got '{actual}'."