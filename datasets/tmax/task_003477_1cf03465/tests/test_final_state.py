# test_final_state.py

import os
import tarfile
import pytest

def test_processing_log_contents():
    log_path = "/home/user/processing_log.txt"
    assert os.path.isfile(log_path), f"Log file missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "Text files modified: 2\nValid binary files: 2"
    assert content == expected_content, f"Log file content incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_final_docs_tarball_exists_and_valid():
    tarball_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(tarball_path), f"Final tarball missing at {tarball_path}"
    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive"

def test_final_docs_tarball_contents():
    tarball_path = "/home/user/final_docs.tar.gz"

    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()

        # Since the user compressed /home/user/organized_docs/, the paths in the tarball might be absolute or relative.
        # We check the basenames and their parent directory names.

        text_files = [n for n in names if n.endswith(".txt") or n.endswith(".md")]
        binary_files = [n for n in names if n.endswith(".bin") or n.endswith(".dat")]

        # Basenames
        text_basenames = {os.path.basename(n) for n in text_files}
        binary_basenames = {os.path.basename(n) for n in binary_files}

        assert text_basenames == {"file1.txt", "file2.md", "file3.txt"}, f"Text files in archive incorrect: {text_basenames}"
        assert binary_basenames == {"legacy1.bin", "legacy3.bin"}, f"Binary files in archive incorrect: {binary_basenames}"

        # Ensure files are in text and binary directories respectively
        for f in text_files:
            assert os.path.basename(os.path.dirname(f)) == "text", f"Text file {f} not in a 'text' directory"

        for f in binary_files:
            assert os.path.basename(os.path.dirname(f)) == "binary", f"Binary file {f} not in a 'binary' directory"

def test_text_files_transformation():
    tarball_path = "/home/user/final_docs.tar.gz"

    with tarfile.open(tarball_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and (member.name.endswith(".txt") or member.name.endswith(".md")):
                f = tar.extractfile(member)
                content = f.read().decode("utf-8")
                assert "AcmeCorp" not in content, f"File {member.name} still contains 'AcmeCorp'"
                if os.path.basename(member.name) in ["file1.txt", "file3.txt"]:
                    assert "ZenithInc" in content, f"File {member.name} does not contain 'ZenithInc' as expected"