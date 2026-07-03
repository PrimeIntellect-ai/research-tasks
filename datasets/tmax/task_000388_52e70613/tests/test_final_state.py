# test_final_state.py

import os
import pytest

def test_organized_directory_exists():
    """Test that the organized directory was created."""
    assert os.path.isdir('/home/user/organized'), "The directory /home/user/organized/ was not created."

def test_organized_files_exist():
    """Test that exactly the expected output files exist in the organized directory."""
    expected_files = {'clean_log_000.txt', 'clean_log_001.txt', 'clean_log_002.txt'}
    actual_files = set(os.listdir('/home/user/organized'))
    assert actual_files == expected_files, f"Expected files {expected_files} in /home/user/organized/, but found {actual_files}."

def test_file_contents_and_encoding():
    """Test that the files have the correct number of lines, are UTF-8 encoded, and have correct content."""

    # Generate the expected lines to compare against
    expected_lines = [f"Line {i:04d}: Legacy project log entry with special char: € é ñ\n" for i in range(1, 1251)]

    file_info = [
        ('clean_log_000.txt', 500, expected_lines[0:500]),
        ('clean_log_001.txt', 500, expected_lines[500:1000]),
        ('clean_log_002.txt', 250, expected_lines[1000:1250]),
    ]

    for filename, expected_line_count, expected_content in file_info:
        filepath = os.path.join('/home/user/organized', filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            pytest.fail(f"File {filename} is not valid UTF-8.")

        assert len(lines) == expected_line_count, f"File {filename} should have {expected_line_count} lines, but has {len(lines)}."

        # Check first and last line of each file as a spot check, or check all lines
        assert lines == expected_content, f"Content of {filename} does not match expected output."