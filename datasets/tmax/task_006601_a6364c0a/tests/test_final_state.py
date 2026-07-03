# test_final_state.py

import os
import re
import pytest

def test_fixed_script_exists_and_executable():
    script_path = "/home/user/pipeline/run_pipeline_fixed.sh"
    assert os.path.isfile(script_path), f"The fixed script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The fixed script {script_path} is not executable."

def test_fixed_script_contents():
    script_path = "/home/user/pipeline/run_pipeline_fixed.sh"
    with open(script_path, "r") as f:
        content = f.read()

    # Check that LD_LIBRARY_PATH is set to lib_modern
    assert "lib_modern" in content, "The fixed script does not appear to set LD_LIBRARY_PATH to the modern library directory."
    assert "lib_legacy" not in content, "The fixed script still references the legacy library directory."

    # Check that it validates files for FATAL_CORRUPTION
    assert "FATAL_CORRUPTION" in content, "The fixed script does not contain the check for 'FATAL_CORRUPTION'."
    assert "Skipping corrupt file:" in content, "The fixed script does not print the required 'Skipping corrupt file:' message."

def test_output_final_exists():
    output_path = "/home/user/pipeline/output_final.txt"
    assert os.path.isfile(output_path), f"The final output file {output_path} does not exist."

def test_output_final_contents():
    output_path = "/home/user/pipeline/output_final.txt"
    with open(output_path, "r") as f:
        lines = f.read().splitlines()

    # We expect 10 lines: 5 valid files * 2 lines each
    # file_6.log should be skipped entirely
    assert len(lines) == 10, f"Expected exactly 10 processed lines in {output_path}, but found {len(lines)}."

    for line in lines:
        assert line.startswith("PROCESSED: Data line "), f"Unexpected line format in output: {line}"
        assert "FATAL_CORRUPTION" not in line, "Corrupted data was not filtered out of the final output."

    # Ensure all expected lines are present (order might vary due to parallel execution or assembly)
    expected_lines = set()
    for i in range(1, 6):
        expected_lines.add(f"PROCESSED: Data line A for file {i}")
        expected_lines.add(f"PROCESSED: Data line B for file {i}")

    actual_lines = set(lines)
    missing = expected_lines - actual_lines
    assert not missing, f"Missing expected lines in the final output: {missing}"