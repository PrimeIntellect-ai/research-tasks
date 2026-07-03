# test_final_state.py
import os
import subprocess
import csv

def test_files_exist():
    """Check that all required files exist."""
    required_files = [
        "/home/user/finite_diff.c",
        "/home/user/pipeline.sh",
        "/home/user/results.csv",
        "/home/user/best_h.txt"
    ]
    for filepath in required_files:
        assert os.path.isfile(filepath), f"Required file {filepath} is missing."

def test_pipeline_executable():
    """Check that pipeline.sh is executable."""
    assert os.access("/home/user/pipeline.sh", os.X_OK), "/home/user/pipeline.sh is not executable."

def test_results_csv_format():
    """Check the format and content of results.csv."""
    with open("/home/user/results.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "results.csv is empty."
    assert rows[0] == ["h", "approx", "error"], f"Incorrect CSV header: {rows[0]}"

    # Check that there are 16 rows of data
    assert len(rows) == 17, f"Expected 1 header + 16 data rows, found {len(rows)} rows."

    # Check that data rows can be parsed as floats
    for i, row in enumerate(rows[1:], start=1):
        assert len(row) == 3, f"Row {i} does not have 3 columns."
        try:
            float(row[0])
            float(row[1])
            float(row[2])
        except ValueError:
            assert False, f"Row {i} contains non-numeric data: {row}"

def test_best_h_correctness():
    """Check that best_h.txt contains the h value with the minimum error from results.csv."""
    min_error = float('inf')
    best_h_from_csv = None

    with open("/home/user/results.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            h_val = row[0]
            try:
                err_val = float(row[2])
                if err_val < min_error:
                    min_error = err_val
                    best_h_from_csv = h_val
            except ValueError:
                pass

    with open("/home/user/best_h.txt", "r") as f:
        best_h_from_file = f.read().strip()

    assert best_h_from_file == best_h_from_csv, f"best_h.txt ({best_h_from_file}) does not match the h with minimum error in results.csv ({best_h_from_csv})."

def test_reproducibility():
    """Run the pipeline script and verify it exits successfully and updates files."""
    # Remove best_h.txt to ensure the script recreates it
    os.remove("/home/user/best_h.txt")

    result = subprocess.run(["bash", "/home/user/pipeline.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile("/home/user/best_h.txt"), "pipeline.sh did not recreate best_h.txt."