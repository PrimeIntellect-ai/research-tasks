# test_final_state.py

import os

def test_tracker_script_exists():
    script_path = '/home/user/tracker.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_archive_file_contains_expected_output():
    archive_file = '/home/user/archive.dat'
    assert os.path.isfile(archive_file), f"The archive file {archive_file} does not exist. Did the script run successfully?"

    with open(archive_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "service1.json:5A3B2C5D",
        "database.csv:3X2Y4Z",
        "cache.json:413223"
    }

    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    assert not missing, f"The archive file is missing the following expected lines: {missing}"

    # Also check that there are no extra unexpected lines if we want to be strict,
    # but the truth script uses issubset, so we will just assert subset.
    assert expected_lines.issubset(actual_lines), f"Expected {expected_lines} to be in {actual_lines}"