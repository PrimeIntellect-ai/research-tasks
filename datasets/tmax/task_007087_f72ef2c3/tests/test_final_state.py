# test_final_state.py

import os
import subprocess
import pytest

def test_clean_data_csv_exists_and_valid():
    clean_data_path = "/home/user/data/clean_data.csv"
    assert os.path.isfile(clean_data_path), f"Cleaned data file not found at {clean_data_path}"

    with open(clean_data_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "clean_data.csv is empty"
    assert "ID,Store_ID,Customers,Sales,Promo" in lines[0], "Header row is missing or incorrect in clean_data.csv"

    for i, line in enumerate(lines):
        assert "NA" not in line, f"Found 'NA' in clean_data.csv on line {i+1}: {line}"

    # Expecting 1 header + 6 valid rows
    assert len(lines) == 7, f"Expected 7 lines in clean_data.csv, found {len(lines)}"

def test_results_txt_exists_and_accurate():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        content = f.read()

    assert "NaN" not in content, "Results file still contains 'NaN'. The C++ bug was not completely fixed."

    # Check for expected computed values
    expected_strings = [
        "Global Beta: 15.54",
        "Store 1 Avg Sales: 1650.25",
        "Store 2 Avg Sales: 3250.00",
        "Store 3 Avg Sales: 875.00"
    ]

    for expected in expected_strings:
        assert expected in content, f"Expected output '{expected}' not found in results.txt"

def test_verify_results_script():
    script_path = "/home/user/verify_results.sh"
    assert os.path.isfile(script_path), f"Test script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Test script at {script_path} is not executable"

    # Run the script and check the exit code
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_results.sh failed with exit code {result.returncode}. Output: {result.stdout} {result.stderr}"