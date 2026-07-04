# test_final_state.py
import os

def test_analyze_script_exists():
    """Test that the analyze.py script was created."""
    script_path = "/home/user/analyze.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_output_file_content():
    """Test that output.txt exists and contains the correct extracted parameters."""
    output_path = "/home/user/output.txt"
    assert os.path.exists(output_path), f"The output file {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_lines = [
        "Frequency: 2.50",
        "Amplitude: 4.19",
        "Phase: 0.51",
        "Offset: 2.01"
    ]

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {output_path}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} of {output_path}. Expected '{expected}', got '{actual}'."