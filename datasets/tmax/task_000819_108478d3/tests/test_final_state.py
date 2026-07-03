# test_final_state.py

import os
import stat
import pytest

def test_executable_exists():
    executable_path = "/home/user/organizer"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    st = os.stat(executable_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File at {executable_path} is not executable"

def test_directories_exist():
    valid_dir = "/home/user/valid_packages"
    outdated_dir = "/home/user/outdated_packages"

    assert os.path.isdir(valid_dir), f"Directory {valid_dir} does not exist"
    assert os.path.isdir(outdated_dir), f"Directory {outdated_dir} does not exist"

def test_valid_packages():
    valid_dir = "/home/user/valid_packages"
    expected_files = [
        "libalpha_v1.10.0.meta",
        "libbeta_v2.0.0.meta",
        "libgamma_v0.10.0.meta"
    ]

    for filename in expected_files:
        file_path = os.path.join(valid_dir, filename)
        assert os.path.isfile(file_path), f"Expected valid package missing: {file_path}"

def test_outdated_packages():
    outdated_dir = "/home/user/outdated_packages"
    expected_files = [
        "libalpha_v1.0.5.meta",
        "libbeta_v1.9.9.meta"
    ]

    for filename in expected_files:
        file_path = os.path.join(outdated_dir, filename)
        assert os.path.isfile(file_path), f"Expected outdated package missing: {file_path}"

def test_ignored_packages():
    valid_dir = "/home/user/valid_packages"
    outdated_dir = "/home/user/outdated_packages"
    ignored_filename = "libdelta_v1.0.0.meta"

    valid_path = os.path.join(valid_dir, ignored_filename)
    outdated_path = os.path.join(outdated_dir, ignored_filename)

    assert not os.path.exists(valid_path), f"Ignored package {ignored_filename} should not be in {valid_dir}"
    assert not os.path.exists(outdated_path), f"Ignored package {ignored_filename} should not be in {outdated_dir}"

def test_run_log_exists():
    log_path = "/home/user/run.log"
    assert os.path.isfile(log_path), f"Run log not found at {log_path}"

def test_file_contents_copied_correctly():
    # Verify that the files copied have the same content as the original ones
    valid_dir = "/home/user/valid_packages"
    raw_dir = "/home/user/packages_raw"

    # libalpha_v1.10.0.meta corresponds to bGliYWxwaGFfdjEuMTAuMC5tZXRh
    raw_path = os.path.join(raw_dir, "bGliYWxwaGFfdjEuMTAuMC5tZXRh")
    copied_path = os.path.join(valid_dir, "libalpha_v1.10.0.meta")

    if os.path.isfile(raw_path) and os.path.isfile(copied_path):
        with open(raw_path, 'r') as f1, open(copied_path, 'r') as f2:
            assert f1.read() == f2.read(), f"Content of {copied_path} does not match the original file"