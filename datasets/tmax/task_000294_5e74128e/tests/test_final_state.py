# test_final_state.py

import os
import tarfile
import pytest

def test_incident_id():
    incident_file = "/home/user/incident_id.txt"
    assert os.path.exists(incident_file), f"File {incident_file} does not exist."
    with open(incident_file, "r") as f:
        content = f.read().strip()
    assert content == "88310", f"Expected incident ID '88310', but got '{content}'."

def test_organized_docs_archive():
    archive_path = "/home/user/organized_docs.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    expected_files = {"intro.md", "setup.md", "api.txt", "build_tool"}

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Check that there are exactly 4 members
        assert len(members) == 4, f"Expected exactly 4 files in the archive, found {len(members)}."

        actual_files = set()
        for member in members:
            # Must be a regular file
            assert member.isfile(), f"Archive member '{member.name}' is not a regular file."
            # Must not contain directory separators (i.e. must be at the root)
            assert "/" not in member.name and "\\" not in member.name, f"File '{member.name}' is not at the root of the archive."
            actual_files.add(member.name)

        assert actual_files == expected_files, f"Archive contents {actual_files} do not match expected {expected_files}."

        # Verify build_tool is an ELF binary
        build_tool_member = tar.getmember("build_tool")
        with tar.extractfile(build_tool_member) as f:
            header = f.read(4)
            assert header == b"\x7fELF", "The 'build_tool' file does not have a valid ELF header."