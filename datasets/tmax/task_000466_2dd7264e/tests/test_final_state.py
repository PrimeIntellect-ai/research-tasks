# test_final_state.py

import os
import tarfile
import pytest

def test_events_directory_removed():
    assert not os.path.exists('/home/user/events'), "The directory /home/user/events/ should have been deleted."

def test_archive_exists_and_valid():
    archive_path = '/home/user/events_archive.tar.gz'
    assert os.path.isfile(archive_path), f"The archive {archive_path} should exist."

    # Check if it's a valid tar.gz file and contains the events directory
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            names = tar.getnames()
            # The tarball should contain 'events' at its root
            assert any(name.startswith('events') for name in names), "The archive must contain the 'events' directory."
    except tarfile.ReadError:
        pytest.fail(f"The file {archive_path} is not a valid gzip-compressed tarball.")

def test_user_durations_content():
    output_path = '/home/user/user_durations.csv'
    assert os.path.isfile(output_path), f"The output file {output_path} should exist."

    expected_lines = [
        "u5,5000",
        "u1,350",
        "u2,150",
        "u4,0"
    ]

    with open(output_path, 'r') as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {output_path} is incorrect. "
        f"Expected:\n{chr(10).join(expected_lines)}\nActual:\n{chr(10).join(actual_lines)}"
    )