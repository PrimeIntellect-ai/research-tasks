# test_final_state.py

import os
import tarfile
import pytest

def test_pigz_compiled_and_copied():
    pigz_path = "/home/user/bin/pigz"
    assert os.path.isfile(pigz_path), f"pigz executable is missing at {pigz_path}."
    assert os.access(pigz_path, os.X_OK), f"pigz at {pigz_path} is not executable."

def test_archive_script_exists():
    script_path = "/home/user/archive.sh"
    assert os.path.isfile(script_path), f"Archive script is missing at {script_path}."
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Archive script at {script_path} must be readable or executable."

def test_archive_file_exists_and_size_metric():
    archive_path = "/home/user/archived_logs.tar.gz"
    assert os.path.isfile(archive_path), f"Target archive file is missing at {archive_path}."

    file_size = os.path.getsize(archive_path)
    threshold = 150000

    assert file_size <= threshold, (
        f"Archive size metric failed: measured {file_size} bytes, "
        f"which is not <= threshold of {threshold} bytes. "
        "Ensure [DEBUG] and [TRACE] lines are stripped and -9 compression is used."
    )

def test_archive_contents_filtered():
    # Verify that the archive is a valid tar.gz and does not contain excluded patterns
    archive_path = "/home/user/archived_logs.tar.gz"
    assert os.path.isfile(archive_path), "Target archive file is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getmembers()
            assert len(members) > 0, "The archive is empty."

            for member in members:
                if member.isfile() and member.name.endswith(".log"):
                    f = tar.extractfile(member)
                    if f is not None:
                        content = f.read().decode('utf-8', errors='replace')
                        assert "[DEBUG]" not in content, f"Found [DEBUG] lines in archived file {member.name}."
                        assert "[TRACE]" not in content, f"Found [TRACE] lines in archived file {member.name}."
    except tarfile.ReadError:
        pytest.fail(f"Could not read {archive_path} as a valid gzip-compressed tar archive.")