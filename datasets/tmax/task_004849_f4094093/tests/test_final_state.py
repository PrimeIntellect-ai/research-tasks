# test_final_state.py

import os
import subprocess
import pytest

def test_c_file_exists():
    """Check that the C source file exists."""
    file_path = "/home/user/src/extractor.c"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_makefile_exists():
    """Check that the Makefile exists."""
    file_path = "/home/user/src/Makefile"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_pipeline_execution_and_output():
    """Run the pipeline via make and verify the output."""
    # Ensure the output directory is clean to verify 'make run' creates it or writes to it
    output_file = "/home/user/output/features.csv"
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run make run
    result = subprocess.run(
        ["make", "run"],
        cwd="/home/user/src",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'make run' failed with return code {result.returncode}.\nstderr: {result.stderr}\nstdout: {result.stdout}"

    # Check if the output file was created
    assert os.path.isfile(output_file), f"Output file {output_file} was not created after running 'make run'."

    # Expected output based on the raw_logs.tsv provided in the truth setup
    expected_lines = [
        "1670000000,S1,2",
        "1670000060,S2,2",
        "1670000120,S1,1",
        "1670000180,S3,0",
        "1670000240,S1,3"
    ]

    with open(output_file, "r") as f:
        actual_content = f.read().strip().splitlines()

    assert len(actual_content) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but got {len(actual_content)}."

    for i, (actual, expected) in enumerate(zip(actual_content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"