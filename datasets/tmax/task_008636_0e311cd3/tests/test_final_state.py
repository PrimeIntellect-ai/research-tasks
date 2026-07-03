# test_final_state.py

import os
import csv
import pytest

def test_analyze_logs_script_exists():
    """Test that the python script was created."""
    script_path = "/home/user/analyze_logs.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_csv_output_exists():
    """Test that the output CSV file was generated."""
    csv_path = "/home/user/fatal_sizes.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} does not exist. Did you run your script?"

def test_csv_output_content():
    """Test that the CSV output contains the correct aggregated data and is properly formatted."""
    csv_path = "/home/user/fatal_sizes.csv"
    if not os.path.isfile(csv_path):
        pytest.fail(f"Cannot check content because {csv_path} is missing.")

    expected_rows = [
        ["archive_name", "total_fatal_bytes"],
        ["logs_A.tar.gz", "50000"],
        ["logs_B.tar.gz", "20000"],
        ["logs_C.tar.gz", "0"],
        ["logs_D.tar.gz", "9999"]
    ]

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Read all non-empty rows and strip any trailing whitespace
        actual_rows = [[cell.strip() for cell in row] for row in reader if row]

    assert actual_rows == expected_rows, (
        f"CSV content does not match expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual:   {actual_rows}"
    )

def test_no_extracted_files():
    """Test that no files were extracted to disk in the logs directory."""
    log_dir = "/home/user/storage/logs"
    if os.path.isdir(log_dir):
        for item in os.listdir(log_dir):
            item_path = os.path.join(log_dir, item)
            assert item.endswith(".tar.gz") and os.path.isfile(item_path), (
                f"Found unexpected item in logs directory: {item_path}. "
                "The task requires reading nested archives in memory without extracting them to disk."
            )