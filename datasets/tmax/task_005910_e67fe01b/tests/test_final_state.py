# test_final_state.py

import os
import tarfile
import pytest

def test_doc_parser_c_exists():
    c_file_path = "/home/user/doc_parser.c"
    assert os.path.isfile(c_file_path), f"The required C program was not found at {c_file_path}"

def test_final_docs_archive_exists():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(archive_path), f"The final archive was not found at {archive_path}"

def test_final_docs_archive_contents():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(archive_path), "Archive missing, cannot check contents"

    expected_files = {
        "installation_guide.txt": b"setup content\n",
        "authentication_v2.txt": b"new api content\n",
        "for_loops_tutorial.txt": b"loop content\n"
    }

    actual_files = {}

    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():
            # The files should be at the root of the archive, no directories
            assert not member.isdir(), f"Archive should not contain directories, found: {member.name}"
            # Ensure no parent paths like 'approved_docs/...'
            assert "/" not in member.name and "\\" not in member.name, f"Archive should only contain flattened files, found nested path: {member.name}"

            f = tar.extractfile(member)
            if f is not None:
                actual_files[member.name] = f.read()

    # Check that exactly the expected files are present
    assert set(actual_files.keys()) == set(expected_files.keys()), (
        f"Archive contents do not match expected. "
        f"Expected: {list(expected_files.keys())}, Found: {list(actual_files.keys())}"
    )

    # Check the contents of each file
    for filename, expected_content in expected_files.items():
        assert actual_files[filename].strip() == expected_content.strip(), (
            f"Content mismatch in {filename}. "
            f"Expected: {expected_content}, Found: {actual_files[filename]}"
        )