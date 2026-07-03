# test_final_state.py

import os
import pytest

def test_symlinks_created():
    mappings = {
        '/home/user/app/input': '/home/user/real_data/input',
        '/home/user/app/output': '/home/user/real_data/output',
        '/home/user/app/logs': '/home/user/real_data/logs',
    }

    for symlink, real_dir in mappings.items():
        assert os.path.exists(real_dir), f"Real directory {real_dir} does not exist."
        assert os.path.islink(symlink), f"{symlink} is not a symlink."
        target = os.readlink(symlink)
        assert target == real_dir, f"Symlink {symlink} points to {target}, expected {real_dir}."

def test_processed_output_exists_and_correct():
    out_file = '/home/user/real_data/output/data1.txt.out'
    assert os.path.isfile(out_file), f"Output file {out_file} does not exist. Did the processor run successfully?"

    with open(out_file, 'r') as f:
        content = f.read().strip()

    expected_content = "Test data to process - PROCESSED"
    assert content == expected_content, f"Output file content is '{content}', expected '{expected_content}'."

def test_log_rotated():
    rotated_log = '/home/user/app/logs/processor.log.1'
    assert os.path.isfile(rotated_log), f"Rotated log file {rotated_log} does not exist. Did the rotation script run?"

    with open(rotated_log, 'r') as f:
        content = f.read()

    assert "INFO: Starting processing." in content, "Rotated log does not contain expected INFO messages."
    assert "ERROR: Mock error for log testing." in content, "Rotated log does not contain expected ERROR messages."

def test_error_summary_created():
    error_summary = '/home/user/app/logs/error_summary.txt'
    assert os.path.isfile(error_summary), f"Error summary file {error_summary} does not exist."

    with open(error_summary, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "Error summary file is empty."
    for line in lines:
        assert "ERROR" in line, f"Found non-error line in error summary: {line.strip()}"

    content = "".join(lines)
    assert "ERROR: Mock error for log testing." in content, "Error summary does not contain the expected mock error."