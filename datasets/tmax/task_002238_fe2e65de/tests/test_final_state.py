# test_final_state.py

import os
import pytest

def test_fixed_output_exists():
    """Test that the fixed output file exists."""
    output_file = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you redirect the output?"

def test_fixed_output_content():
    """Test that the fixed output file contains the correct calculated values."""
    output_file = "/home/user/fixed_output.txt"
    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Total Time: 100.875",
        "Uptime: 90.500",
        "Percentage: 89.714994"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == 3, f"Expected 3 lines of output, got {len(actual_lines)}."

    assert actual_lines[0] == expected_lines[0], f"Expected '{expected_lines[0]}', got '{actual_lines[0]}'."
    assert actual_lines[1] == expected_lines[1], f"Expected '{expected_lines[1]}', got '{actual_lines[1]}'."

    # For percentage, allow a tiny bit of flexibility if they used %g or similar, but exact match is preferred based on spec.
    # The spec says "exactly match the output format of the original program", which uses %.6f
    assert actual_lines[2] == expected_lines[2], f"Expected '{expected_lines[2]}', got '{actual_lines[2]}'."

def test_monitor_c_modifications():
    """Test that monitor.c was modified to fix the bugs."""
    source_file = "/home/user/monitor.c"
    assert os.path.isfile(source_file), f"Source file {source_file} is missing."

    with open(source_file, "r") as f:
        content = f.read()

    # Check if double is used instead of float for precision
    assert "double" in content, "The source code does not seem to use 'double' precision, which is necessary to fix the numerical instability."

    # Check if the feof loop was fixed (typically by checking fscanf return value or breaking on "END")
    # We won't strictly enforce how they fixed it, but the output test will catch if they didn't.