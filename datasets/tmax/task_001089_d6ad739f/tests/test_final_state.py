# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_compilation_and_execution():
    """Test that the Makefile compiles the C program and generates the output."""
    pipeline_dir = '/home/user/pipeline'

    assert os.path.isfile(os.path.join(pipeline_dir, 'Makefile')), "Makefile is missing in /home/user/pipeline."
    assert os.path.isfile(os.path.join(pipeline_dir, 'process.c')), "process.c is missing in /home/user/pipeline."

    # Run make
    result = subprocess.run(['make', '-C', pipeline_dir, 'all'], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}\n{result.stdout}"

    # Verify executable exists
    assert os.path.isfile(os.path.join(pipeline_dir, 'process')), "Executable 'process' was not created by make."

def test_training_data_output():
    """Test that the output CSV matches the expected dimensionality reduction results."""
    output_file = '/home/user/output/training_data.csv'

    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Make sure the C program generates it."

    expected_csv = "id,PC1,PC2\n2,72.0,10.0\n3,82.0,10.0\n5,30.0,10.0\n"

    with open(output_file, 'r') as f:
        content = f.read()

    # Normalize line endings and strip trailing whitespace
    actual_lines = [line.strip() for line in content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_csv.strip().splitlines()]

    assert actual_lines == expected_lines, (
        f"Content of {output_file} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )