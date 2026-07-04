# test_final_state.py

import os
import hashlib
import tarfile
import pytest

def get_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_cpp_files_exist():
    assert os.path.isfile("/home/user/tracker.cpp"), "/home/user/tracker.cpp is missing."
    assert os.path.isfile("/home/user/tracker"), "/home/user/tracker executable is missing."
    assert os.access("/home/user/tracker", os.X_OK), "/home/user/tracker is not executable."

def test_manifest_v2_correctness():
    manifest_path = "/home/user/manifest_v2.txt"
    assert os.path.isfile(manifest_path), f"{manifest_path} is missing."

    # Calculate expected checksums
    sha_a = get_sha256("/home/user/gcode_current/partA.gcode")
    sha_b = get_sha256("/home/user/gcode_current/partB.gcode")
    sha_c = get_sha256("/home/user/gcode_current/partC.gcode")

    expected_lines = [
        f"partA.gcode,1.0,{sha_a}",
        f"partB.gcode,1.2,{sha_b}",
        f"partC.gcode,2.0,{sha_c}"
    ]

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest contents are incorrect or not sorted properly.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}"
    )

def test_incremental_archive():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"{archive_path} is not a valid gzip-compressed tarball.")

    expected_files = {"partB.gcode", "partC.gcode"}
    actual_files = set(names)

    assert actual_files == expected_files, (
        f"Archive contents do not match expected NEW_OR_CHANGED files at the root.\n"
        f"Expected exactly: {expected_files}\n"
        f"Found: {actual_files}"
    )