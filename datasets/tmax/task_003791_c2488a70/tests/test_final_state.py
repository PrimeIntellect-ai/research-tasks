# test_final_state.py

import os
import tarfile
import tempfile

def test_final_docs_archive_exists_and_valid():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar file."

def test_final_docs_content():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(tmpdir)

        # Find the files, they could be nested
        found_files = {}
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file in ["readme.txt", "arch.md", "notes.txt"]:
                    found_files[file] = os.path.join(root, file)

        assert "readme.txt" in found_files, "readme.txt not found in final_docs.tar.gz"
        assert "arch.md" in found_files, "arch.md not found in final_docs.tar.gz"
        assert "notes.txt" in found_files, "notes.txt not found in final_docs.tar.gz"

        with open(found_files["readme.txt"], "r") as f:
            content = f.read().strip()
            expected = "Welcome to NovaTech.&4&This is v2.2 of our software."
            assert content == expected, f"readme.txt content is incorrect. Expected: '{expected}', Got: '{content}'"

        with open(found_files["arch.md"], "r") as f:
            content = f.read().strip()
            expected = "NovaTech v2.2 architecture:  Client ->   Server."
            assert content == expected, f"arch.md content is incorrect. Expected: '{expected}', Got: '{content}'"

        with open(found_files["notes.txt"], "r") as f:
            content = f.read().strip()
            expected = "&5&Indent test for NovaTech v2.2."
            assert content == expected, f"notes.txt content is incorrect. Expected: '{expected}', Got: '{content}'"

def test_cpp_program_exists():
    assert os.path.exists("/home/user/compressor.cpp"), "/home/user/compressor.cpp does not exist."
    assert os.path.exists("/home/user/compressor"), "/home/user/compressor executable does not exist."
    assert os.access("/home/user/compressor", os.X_OK), "/home/user/compressor is not executable."