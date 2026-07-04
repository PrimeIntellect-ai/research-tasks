# test_final_state.py

import os
import stat
import zipfile
import pytest

def test_curate_script_exists_and_executable():
    """Check that curate.sh exists and is executable."""
    script_path = '/home/user/curate.sh'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_zip_archive_exists_and_valid():
    """Check that the curated_artifacts.zip exists and is a valid zip archive."""
    zip_path = '/home/user/curated_artifacts.zip'
    assert os.path.exists(zip_path), f"The archive {zip_path} does not exist."
    assert os.path.isfile(zip_path), f"The path {zip_path} is not a file."
    assert zipfile.is_zipfile(zip_path), f"The file {zip_path} is not a valid zip archive."

def test_zip_archive_contents():
    """Check that the zip archive contains the correct files at the correct paths."""
    zip_path = '/home/user/curated_artifacts.zip'
    assert os.path.exists(zip_path), f"The archive {zip_path} does not exist."

    with zipfile.ZipFile(zip_path, 'r') as z:
        # Extract files, ignoring directory entries
        files = [info.filename for info in z.infolist() if not info.is_dir()]

        # Clean up paths (e.g., remove leading './' if the student used `zip -r archive.zip .`)
        cleaned_files = set()
        for f in files:
            cf = f
            if cf.startswith('./'):
                cf = cf[2:]
            cleaned_files.add(cf)

        expected_files = {
            'elf/arm_app1',
            'gcode/print1.gcode',
            'wal/db1.wal',
            'wal/db2.wal'
        }

        # Verify all expected files are present
        for ef in expected_files:
            assert ef in cleaned_files, (
                f"Expected file '{ef}' not found in the root of the zip archive. "
                f"Make sure paths are relative to /home/user/curated. Found files: {cleaned_files}"
            )

        # Verify no incorrectly classified files are present
        excluded_names = ['x86_app', 'print2.gcode', 'db3.wal', 'readme.txt']
        for cf in cleaned_files:
            for ex in excluded_names:
                assert ex not in cf, (
                    f"File '{ex}' should not be in the curated zip archive, but found '{cf}'. "
                    f"Check your classification logic."
                )