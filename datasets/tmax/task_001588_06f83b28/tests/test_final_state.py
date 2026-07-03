# test_final_state.py

import os
import json
import stat
import pytest

def test_builder_script_exists():
    path = "/home/user/builder.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_release_dir_exists():
    path = "/home/user/release"
    assert os.path.isdir(path), f"The directory {path} does not exist."

def test_auth_svc_executable():
    path = "/home/user/release/auth_svc_23"
    assert os.path.isfile(path), f"The compiled executable {path} does not exist."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {path} is not executable."

    # Check for ELF magic bytes
    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"The file {path} is not a valid ELF binary."

def test_data_svc_executable():
    path = "/home/user/release/data_svc_20"
    assert os.path.isfile(path), f"The compiled executable {path} does not exist."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {path} is not executable."

    # Check for ELF magic bytes
    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"The file {path} is not a valid ELF binary."

def test_release_log_json():
    path = "/home/user/release_log.json"
    assert os.path.isfile(path), f"The log file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    expected = {"auth_svc": 23, "data_svc": 20}
    assert data == expected, f"The contents of {path} do not match the expected output. Got: {data}"