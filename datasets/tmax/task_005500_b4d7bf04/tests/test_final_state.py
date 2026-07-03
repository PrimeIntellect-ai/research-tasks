# test_final_state.py

import os
import pytest

def test_malicious_file_skipped():
    # The script should not have extracted hacked.txt outside the extracted directory
    assert not os.path.exists("/home/user/hacked.txt"), "Malicious file was extracted outside the intended directory!"
    assert not os.path.exists("/home/user/extracted/../hacked.txt"), "Malicious file was extracted outside the intended directory via path traversal!"

def test_valid_files_extracted():
    expected_files = [
        "/home/user/extracted/test1.gcode",
        "/home/user/extracted/subdir/test2.gcode",
        "/home/user/extracted/data/test3.gcode"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Valid file {f} was not extracted correctly."

def test_symlinks_created_and_correct():
    expected_symlinks = {
        "/home/user/organized/calibration/test1.gcode": "/home/user/extracted/test1.gcode",
        "/home/user/organized/calibration/test3.gcode": "/home/user/extracted/data/test3.gcode",
        "/home/user/organized/production/test2.gcode": "/home/user/extracted/subdir/test2.gcode"
    }

    for symlink, target in expected_symlinks.items():
        assert os.path.islink(symlink), f"Expected symlink {symlink} does not exist or is not a symlink."
        actual_target = os.readlink(symlink)
        assert actual_target == target, f"Symlink {symlink} points to {actual_target}, expected {target}."

def test_verification_log():
    log_path = "/home/user/symlink_report.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/organized/calibration/test1.gcode -> /home/user/extracted/test1.gcode",
        "/home/user/organized/calibration/test3.gcode -> /home/user/extracted/data/test3.gcode",
        "/home/user/organized/production/test2.gcode -> /home/user/extracted/subdir/test2.gcode"
    ]

    # Check if lines match exactly
    assert lines == expected_lines, f"Log file contents do not match the expected sorted format. Got: {lines}"