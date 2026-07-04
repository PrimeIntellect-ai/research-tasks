# test_final_state.py

import os
import pytest

def test_repo_bin_exists():
    path = "/home/user/repo.bin"
    assert os.path.isfile(path), f"The archive file {path} does not exist."

def test_repo_bin_size():
    path = "/home/user/repo.bin"
    assert os.path.isfile(path), f"The archive file {path} does not exist."

    size = os.path.getsize(path)
    threshold = 2500000
    assert size <= threshold, f"Archive size is {size} bytes, which exceeds the threshold of {threshold} bytes. Compression may have failed or not been applied."

def test_incoming_directory_empty():
    path = "/home/user/incoming"
    assert os.path.isdir(path), f"Incoming directory {path} is missing."

    files = os.listdir(path)
    assert len(files) == 0, f"Incoming directory is not empty. Unprocessed files: {files}"

def test_cmake_fixed():
    path = "/app/vendor/snappy-1.1.10/CMakeLists.txt"
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
        assert "set(CMAKE_CXX_STANDARD 98)" not in content, "The CMakeLists.txt file still contains the C++98 perturbation."

def test_snappy_installed():
    lib_path1 = "/home/user/local/lib/libsnappy.a"
    lib_path2 = "/home/user/local/lib/libsnappy.so"
    lib_path3 = "/home/user/local/lib64/libsnappy.a"
    lib_path4 = "/home/user/local/lib64/libsnappy.so"

    installed = any(os.path.isfile(p) for p in [lib_path1, lib_path2, lib_path3, lib_path4])
    assert installed, "Snappy library does not appear to be installed in /home/user/local/lib or lib64."