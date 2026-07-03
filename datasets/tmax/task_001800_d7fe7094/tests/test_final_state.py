# test_final_state.py

import os
import subprocess
import pytest

def test_run_sh_exists_and_executable():
    """Check if run.sh exists and is executable."""
    script_path = "/home/user/pipeline/run.sh"
    assert os.path.isfile(script_path), f"Master script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Master script {script_path} is not executable."

def test_pipeline_execution():
    """Execute the pipeline script and ensure it returns a 0 exit code."""
    script_path = "/home/user/pipeline/run.sh"
    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_processed_configs_directory():
    """Check that the processed_configs directory contains the correct files."""
    processed_dir = "/home/user/processed_configs"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    files = set(os.listdir(processed_dir))
    expected_files = {"alpha.txt", "beta.txt", "gamma.txt"}

    assert "delta.txt" not in files, "delta.txt should have been skipped due to ERROR_ key."
    assert expected_files.issubset(files), f"Missing expected processed files. Found: {files}"

def test_processed_configs_content():
    """Check that the processed configs are correctly normalized and sorted."""
    expected_alpha = ["CACHE_SIZE=1024", "DB_HOST=10.0.0.1", "DB_PORT=5432", "MAX_RETRIES=3"]
    expected_beta = ["CACHE_SIZE=2048", "DB_HOST=10.0.0.2", "DB_PORT=5432", "TIMEOUT=30"]
    expected_gamma = ["DB_HOST=10.0.0.3", "DB_PORT=5432", "MAX_RETRIES=5", "TIMEOUT=60"]

    def check_file(filename, expected_lines):
        filepath = f"/home/user/processed_configs/{filename}"
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        assert lines == expected_lines, f"Content of {filename} is incorrect or not sorted properly.\nExpected: {expected_lines}\nGot: {lines}"

    check_file("alpha.txt", expected_alpha)
    check_file("beta.txt", expected_beta)
    check_file("gamma.txt", expected_gamma)

def test_config_matrix_csv():
    """Check that the final joined CSV matrix is exactly as expected."""
    csv_path = "/home/user/output/config_matrix.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} is missing."

    expected_csv_lines = [
        "KEY,alpha,beta,gamma",
        "CACHE_SIZE,1024,2048,",
        "DB_HOST,10.0.0.1,10.0.0.2,10.0.0.3",
        "DB_PORT,5432,5432,5432",
        "MAX_RETRIES,3,,5",
        "TIMEOUT,,30,60"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_csv_lines, f"CSV content does not match expected output.\nExpected:\n{expected_csv_lines}\nGot:\n{actual_lines}"