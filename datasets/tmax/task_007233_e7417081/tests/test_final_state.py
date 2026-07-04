# test_final_state.py

import os
import tarfile
import pytest

def test_script_exists_and_uses_tempfile():
    script_path = "/home/user/organize.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()
    assert "tempfile" in content, "The script does not seem to use the 'tempfile' module as required."

def test_organized_src_directory():
    dest_dir = "/home/user/organized_src"
    assert os.path.isdir(dest_dir), f"Directory {dest_dir} does not exist."

    expected_files = {
        "src_main.py": "print('main')\n",
        "src_utils.py": "print('utils')\n",
        "src_auth.py": "print('auth')\n",
        "src_db.py": "print('db')\n"
    }

    actual_files = os.listdir(dest_dir)

    # Check that all expected files exist and have correct content
    for fname, expected_content in expected_files.items():
        assert fname in actual_files, f"Expected file {fname} not found in {dest_dir}."
        with open(os.path.join(dest_dir, fname), "r") as f:
            content = f.read()
        assert expected_content.strip() in content.strip(), f"Content of {fname} is incorrect."

    # Check that no other unexpected files are present
    for fname in actual_files:
        assert fname in expected_files, f"Unexpected file {fname} found in {dest_dir}."

def test_archive_exists_and_contents():
    archive_path = "/home/user/src_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    expected_filenames = ["src_main.py", "src_utils.py", "src_auth.py", "src_db.py"]

    with tarfile.open(archive_path, "r:gz") as tar:
        tar_names = tar.getnames()

        # Check that expected files are in the tarball (ignoring directory prefixes)
        basenames = [os.path.basename(name) for name in tar_names]
        for expected in expected_filenames:
            assert expected in basenames, f"Expected file {expected} not found in archive {archive_path}."