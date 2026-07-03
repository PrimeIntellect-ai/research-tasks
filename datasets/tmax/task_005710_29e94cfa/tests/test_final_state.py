# test_final_state.py
import os
import gzip
import pytest

def test_script_exists():
    script_path = "/home/user/process_artifacts.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_file_exists():
    output_path = "/home/user/corrupted_report.txt.gz"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_output_file_content():
    output_path = "/home/user/corrupted_report.txt.gz"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    try:
        with gzip.open(output_path, "rt", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as a UTF-8 encoded gzip file: {e}")

    # Clean up whitespace/newlines
    lines = [line.strip() for line in lines if line.strip()]

    expected_lines = [
        "[STATE: CORRUPTED] artifact X-102 checksum failed",
        "[STATE: CORRUPTED] artifact Y-201 invalid header"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but found {len(lines)} in {output_path}."

    for expected_line in expected_lines:
        assert expected_line in lines, f"Expected line '{expected_line}' not found in the output."

    # Verify no other lines are present
    for line in lines:
        assert line in expected_lines, f"Unexpected line '{line}' found in the output."