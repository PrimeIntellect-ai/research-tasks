# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_script_exists():
    """Check if pipeline.sh exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Script not found: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_venv_and_csvkit_installed():
    """Check if the virtual environment exists and csvkit is installed."""
    venv_python = "/home/user/venv/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}"

    # Check if csvkit is installed in the venv
    try:
        result = subprocess.run(
            ["/home/user/venv/bin/pip", "show", "csvkit"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        assert "Name: csvkit" in result.stdout, "csvkit does not appear to be installed in the virtual environment."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run pip show csvkit in the virtual environment. Is csvkit installed?")

def test_clean_tokens_csv():
    """Check if clean_tokens.csv contains the expected cleaned and tokenized data."""
    file_path = "/home/user/clean_tokens.csv"
    assert os.path.exists(file_path), f"Output file not found: {file_path}"

    expected_content = """item_id,publish_date,tokens
1,2023-01-15,hello world great item
4,2023-04-20,testing pipeline reproducibility
5,2023-05-05,just letters and spaces
6,2023-06-12,extra spaces everywhere"""

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"The contents of {file_path} do not match the expected output."

def test_row_count_txt():
    """Check if row_count.txt contains the correct integer."""
    file_path = "/home/user/row_count.txt"
    assert os.path.exists(file_path), f"Output file not found: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "4", f"Expected row_count.txt to contain '4', but found '{content}'."