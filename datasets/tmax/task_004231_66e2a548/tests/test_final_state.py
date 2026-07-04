# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_lockfile_exists():
    lockfile_path = "/home/user/project/lockfile.csv"
    assert os.path.isfile(lockfile_path), f"Lockfile {lockfile_path} does not exist. The script failed to generate it."

def test_lockfile_contents():
    lockfile_path = "/home/user/project/lockfile.csv"
    assert os.path.isfile(lockfile_path), "Lockfile not found."

    # Compute expected SHA256 checksums from the actual files
    cl_path = "/home/user/project/downloads/core_logger-1.2.0.tar.gz"
    hc_path = "/home/user/project/downloads/http_client-2.1.0.tar.gz"
    nu_path = "/home/user/project/downloads/network_utils-1.1.0.tar.gz"

    assert os.path.isfile(cl_path), f"Tarball {cl_path} is missing."
    assert os.path.isfile(hc_path), f"Tarball {hc_path} is missing."
    assert os.path.isfile(nu_path), f"Tarball {nu_path} is missing."

    sha_cl = get_sha256(cl_path)
    sha_hc = get_sha256(hc_path)
    sha_nu = get_sha256(nu_path)

    expected_lines = [
        f"core_logger,1.2.0,{sha_cl}",
        f"http_client,2.1.0,{sha_hc}",
        f"network_utils,1.1.0,{sha_nu}"
    ]

    with open(lockfile_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Lockfile has {len(actual_lines)} lines, but expected {len(expected_lines)} lines. "
        f"Actual contents: {actual_lines}"
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} of lockfile is incorrect.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

def test_resolver_script_executable():
    script_path = "/home/user/project/resolver.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."