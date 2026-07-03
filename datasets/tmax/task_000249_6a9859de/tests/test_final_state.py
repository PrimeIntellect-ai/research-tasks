# test_final_state.py

import os

def test_backup_chunks_exist_and_correct():
    backup_dir = "/home/user/backup_chunks"

    # Ensure the directory exists
    assert os.path.isdir(backup_dir), f"Directory {backup_dir} does not exist."

    # Expected files
    expected_files = ["xaa", "xab", "xac"]

    # Get actual files in the directory
    actual_files = os.listdir(backup_dir)

    # Check that exactly the expected files are present
    assert set(actual_files) == set(expected_files), (
        f"Expected exactly files {expected_files} in {backup_dir}, "
        f"but found {actual_files}."
    )

    # File contents to check
    expected_contents = {
        "xaa": "A" * 100,
        "xab": ("A" * 20) + ("C" * 80),
        "xac": "C" * 50
    }

    for filename, expected_content in expected_contents.items():
        filepath = os.path.join(backup_dir, filename)

        assert os.path.isfile(filepath), f"Expected file {filepath} is missing."

        # Check size
        actual_size = os.path.getsize(filepath)
        expected_size = len(expected_content)
        assert actual_size == expected_size, (
            f"File {filepath} has incorrect size. Expected {expected_size}, got {actual_size}."
        )

        # Check content
        with open(filepath, "r") as f:
            actual_content = f.read()

        assert actual_content == expected_content, (
            f"File {filepath} has incorrect content."
        )