# test_final_state.py

import os
import subprocess
import pytest

def test_archive_exists_and_size_metric():
    archive_path = "/home/user/docs_backup.tar.gz.enc"

    assert os.path.exists(archive_path), f"Archive not found at {archive_path}"
    assert os.path.isfile(archive_path), f"Expected {archive_path} to be a file"

    size = os.path.getsize(archive_path)

    assert size > 100, f"Archive size {size} bytes is too small (<= 100 bytes). Archive might be empty."
    assert size < 2048, f"Archive size metric {size} bytes is outside the threshold (< 2048 bytes). Symlink loop likely followed."

def test_verify_script_exists_and_works():
    script_path = "/home/user/verify.sh"
    archive_path = "/home/user/docs_backup.tar.gz.enc"

    assert os.path.exists(script_path), f"Verification script not found at {script_path}"
    assert os.path.isfile(script_path), f"Expected {script_path} to be a file"

    # Run the verification script
    result = subprocess.run(["/bin/bash", script_path, archive_path], capture_output=True, text=True)

    assert result.returncode == 0, (
        f"verify.sh failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )