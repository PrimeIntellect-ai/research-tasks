# test_final_state.py

import os
import pytest

def test_go_code_exists_and_uses_atomic_writes():
    go_file = "/home/user/doc_builder.go"
    assert os.path.isfile(go_file), f"Go source file {go_file} is missing."

    with open(go_file, 'r') as f:
        content = f.read()

    assert "os.Rename" in content, "The Go program does not appear to use os.Rename for atomic writes."

def test_output_files_exist_and_have_correct_line_counts():
    dist_dir = "/home/user/dist"
    assert os.path.isdir(dist_dir), f"Output directory {dist_dir} is missing."

    expected_files = {
        "getting_started_part1.md": 50,
        "getting_started_part2.md": 20,
        "networking_part1.md": 50,
        "networking_part2.md": 50,
        "networking_part3.md": 20,
        "api_ref.md": 30
    }

    actual_files = set(os.listdir(dist_dir))

    # Check that all expected files exist
    for filename, expected_lines in expected_files.items():
        filepath = os.path.join(dist_dir, filename)
        assert os.path.isfile(filepath), f"Expected output file {filename} is missing."

        with open(filepath, 'r') as f:
            lines = f.readlines()
        assert len(lines) == expected_lines, f"File {filename} should have {expected_lines} lines, but has {len(lines)}."

    # Check that no unexpected files exist
    unexpected = actual_files - set(expected_files.keys())
    assert not unexpected, f"Unexpected files found in {dist_dir}: {unexpected}"

def test_output_file_contents():
    dist_dir = "/home/user/dist"

    # helper to check lines are a sequence of strings
    def check_sequence(filename, start, end):
        filepath = os.path.join(dist_dir, filename)
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        expected = [str(i) for i in range(start, end + 1)]
        assert lines == expected, f"Content of {filename} does not match expected sequence from {start} to {end}."

    # getting_started parts
    check_sequence("getting_started_part1.md", 1, 50)
    check_sequence("getting_started_part2.md", 51, 70)

    # networking parts
    check_sequence("networking_part1.md", 1, 50)
    check_sequence("networking_part2.md", 51, 100)
    check_sequence("networking_part3.md", 101, 120)

    # api_ref
    check_sequence("api_ref.md", 1, 30)