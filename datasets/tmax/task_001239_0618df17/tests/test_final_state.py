# test_final_state.py

import os
import subprocess
import hashlib
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_pipeline():
    """
    Fixture to ensure the pipeline is executed before running the tests.
    It checks if run.sh exists and is executable, then runs it.
    """
    run_script = "/home/user/run.sh"
    assert os.path.exists(run_script), f"{run_script} does not exist."
    assert os.access(run_script, os.X_OK), f"{run_script} is not executable."

    result = subprocess.run(
        [run_script], 
        cwd="/home/user", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, (
        f"Execution of {run_script} failed with return code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_category_stats_csv():
    """
    Verifies that category_stats.csv contains the correct aggregated data,
    sorted alphabetically by category and rounded to 2 decimal places.
    """
    file_path = "/home/user/category_stats.csv"
    assert os.path.exists(file_path), f"{file_path} does not exist."

    expected_lines = [
        "category,avg_price",
        "Electronics,45.99",
        "Hardware,5.25",
        "Tools,14.38"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected output. "
        f"Expected: {expected_lines}, but got: {actual_lines}"
    )

def test_recommendations_txt():
    """
    Verifies that recommendations.txt contains the correct top 3 recommended
    product IDs for P001 based on Jaccard similarity.
    """
    file_path = "/home/user/recommendations.txt"
    assert os.path.exists(file_path), f"{file_path} does not exist."

    expected_lines = ["P007", "P005", "P002"]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected recommendations. "
        f"Expected: {expected_lines}, but got: {actual_lines}"
    )

def test_checksums_txt():
    """
    Verifies that checksums.txt exists and contains the correct SHA-256
    checksums for both category_stats.csv and recommendations.txt.
    """
    checksums_file = "/home/user/checksums.txt"
    cat_file = "/home/user/category_stats.csv"
    rec_file = "/home/user/recommendations.txt"

    assert os.path.exists(checksums_file), f"{checksums_file} does not exist."
    assert os.path.exists(cat_file), f"{cat_file} does not exist to compute checksum."
    assert os.path.exists(rec_file), f"{rec_file} does not exist to compute checksum."

    def compute_sha256(path):
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    expected_cat_sha = compute_sha256(cat_file)
    expected_rec_sha = compute_sha256(rec_file)

    with open(checksums_file, "r") as f:
        content = f.read()

    assert expected_cat_sha in content, (
        f"SHA-256 hash for category_stats.csv ({expected_cat_sha}) "
        f"was not found in {checksums_file}."
    )
    assert expected_rec_sha in content, (
        f"SHA-256 hash for recommendations.txt ({expected_rec_sha}) "
        f"was not found in {checksums_file}."
    )

    # Ensure the filenames are also mentioned in the checksums file
    assert "category_stats.csv" in content, (
        f"Filename 'category_stats.csv' was not found in {checksums_file}."
    )
    assert "recommendations.txt" in content, (
        f"Filename 'recommendations.txt' was not found in {checksums_file}."
    )