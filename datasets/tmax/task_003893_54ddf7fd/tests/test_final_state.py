# test_final_state.py
import os

def test_archiver_c_exists():
    assert os.path.isfile("/home/user/archiver.c"), "/home/user/archiver.c is missing"

def test_archiver_executable_exists():
    assert os.path.isfile("/home/user/archiver"), "/home/user/archiver is missing"
    assert os.access("/home/user/archiver", os.X_OK), "/home/user/archiver is not executable"

def test_organized_archive_rle():
    archive_path = "/home/user/organized_archive.rle"
    assert os.path.isfile(archive_path), f"{archive_path} is missing"

    expected_content = (
        "---fileA.txt---\n"
        "A5B5C5\n"
        "---fileB.txt---\n"
        "h1e1l2o3 1w1o1r1l1d3\n"
        "---fileC.txt---\n"
        "l1i1n1e113\n"
        "1l1i1n1e123\n"
        "1\n"
    )

    with open(archive_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {archive_path} does not match expected RLE format. Got:\n{actual_content}"