# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_run_script_and_evaluate_accuracy():
    script_path = "/home/user/run_test.sh"
    archive_path = "/home/user/archive.csv"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Run the script to generate the archive.csv
    try:
        subprocess.run(["bash", script_path], timeout=20, check=True)
    except subprocess.TimeoutExpired:
        pytest.fail(f"The script {script_path} timed out after 20 seconds.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The script {script_path} failed with exit code {e.returncode}.")

    assert os.path.exists(archive_path), f"Output file {archive_path} does not exist."

    valid_count = 0
    total_expected = 5000

    with open(archive_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                seq, text = row
                if seq.isdigit():
                    valid_count += 1

    accuracy = valid_count / float(total_expected)

    assert accuracy >= 0.95, f"Accuracy {accuracy:.4f} is below threshold 0.95. Valid lines: {valid_count}/{total_expected}"

def test_executable_exists():
    archiver_path = "/home/user/archiver"
    assert os.path.exists(archiver_path), f"Archiver executable {archiver_path} does not exist."
    assert os.access(archiver_path, os.X_OK), f"Archiver {archiver_path} is not executable."