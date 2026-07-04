# test_final_state.py

import os
import tarfile
import re
import pytest

EXPECTED_FILES = [
    "/home/user/data_to_backup/a.txt",
    "/home/user/data_to_backup/b.bin",
    "/home/user/data_to_backup/dir1/c.txt",
    "/home/user/data_to_backup/dir2/d.txt",
]

def test_backup_log_exists_and_correct():
    log_path = "/home/user/backup_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_FILES, (
        f"Contents of {log_path} do not match the expected sorted list of real absolute paths.\n"
        f"Expected: {EXPECTED_FILES}\n"
        f"Got: {lines}"
    )

def test_tarball_exists_and_valid():
    tar_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(tar_path), f"Tarball {tar_path} is missing."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            members = tar.getnames()
    except Exception as e:
        pytest.fail(f"Failed to open or read {tar_path} as a gzip-compressed tar archive: {e}")

    # Tarfile often strips leading slashes for safety. We should tolerate both.
    expected_names_stripped = [p.lstrip("/") for p in EXPECTED_FILES]

    sorted_members = sorted(members)

    # Check if members match either absolute paths or stripped paths
    if sorted_members != EXPECTED_FILES and sorted_members != expected_names_stripped:
        pytest.fail(
            f"Tarball {tar_path} does not contain the correct files.\n"
            f"Expected (absolute): {EXPECTED_FILES}\n"
            f"Or (stripped): {expected_names_stripped}\n"
            f"Got: {sorted_members}"
        )

def test_script_atomic_rename():
    script_path = "/home/user/safe_backup.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Look for atomic rename patterns
    pattern = r"(os\.rename|os\.replace|shutil\.move|Path\.rename|rename\()"
    assert re.search(pattern, content), (
        f"Script {script_path} does not appear to use an atomic rename operation "
        "(e.g., os.rename, shutil.move, Path.rename) to finalize the tarball."
    )