# test_final_state.py
import os

def test_gcode_summary_exists():
    """Check if the gcode_summary.txt file exists."""
    file_path = "/home/user/gcode_summary.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The Go program must generate this file."

def test_gcode_summary_content():
    """Check if the gcode_summary.txt file contains the correct output."""
    file_path = "/home/user/gcode_summary.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    expected_lines = [
        "bracket.gcode: 4",
        "gear.gcode: 3",
        "spacer.gcode: 0"
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_go_program_exists():
    """Check if the Go source file exists."""
    file_path = "/home/user/process_gcode.go"
    assert os.path.isfile(file_path), f"The Go program {file_path} is missing."