# test_final_state.py

import os
import pytest

def test_temperatures_log_exists():
    """Verify that the output file temperatures.log was created."""
    output_path = '/home/user/temperatures.log'
    assert os.path.exists(output_path), f"The output file {output_path} was not created."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

def test_temperatures_log_content():
    """Verify that the output file contains the correct extracted lines."""
    output_path = '/home/user/temperatures.log'

    expected_lines = [
        "shadow_fake.gcode: M109 S210 ; set temp",
        "part2.gcode: M109 S215",
        "part2.gcode: M109 S220 ; higher temp for later"
    ]

    with open(output_path, 'r', encoding='utf-8') as f:
        actual_lines = f.read().splitlines()

    # Remove any trailing whitespace or empty lines if present, though the spec says exact spacing.
    # We will just compare the non-empty stripped lines for robustness, or exact lines.
    actual_lines = [line for line in actual_lines if line]

    assert sorted(actual_lines) == sorted(expected_lines), (
        f"The contents of {output_path} do not match the expected output.\n"
        f"Expected: {sorted(expected_lines)}\n"
        f"Actual: {sorted(actual_lines)}"
    )

def test_no_files_extracted():
    """Verify that the malicious files were not extracted to disk."""
    # Check if the malicious paths were extracted to the root filesystem
    assert not os.path.exists('/etc/shadow_fake.gcode'), "Malicious file was extracted to /etc/shadow_fake.gcode!"
    assert not os.path.exists('/project/subdir/part2.gcode'), "Malicious file was extracted to /project/subdir/part2.gcode!"
    assert not os.path.exists('/var/tmp/notes.txt'), "File was extracted to /var/tmp/notes.txt!"