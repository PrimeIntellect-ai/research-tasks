# test_final_state.py

import os
import pytest

def test_directories_created():
    base_dir = "/home/user/sec_api"
    assert os.path.isdir(base_dir), f"Directory {base_dir} is missing."
    for sub in ["src", "include", "patches", "build"]:
        dir_path = os.path.join(base_dir, sub)
        assert os.path.isdir(dir_path), f"Subdirectory {dir_path} is missing."

def test_files_moved_and_patched():
    src_file = "/home/user/sec_api/src/api_server.cpp"
    include_file = "/home/user/sec_api/include/payload_validator.h"
    patch_file = "/home/user/sec_api/patches/b64_decoder.patch"

    assert os.path.isfile(src_file), f"Source file {src_file} is missing. Was it moved?"
    assert os.path.isfile(include_file), f"Header file {include_file} is missing. Was it moved?"
    assert os.path.isfile(patch_file), f"Patch file {patch_file} is missing. Was it moved?"

    with open(src_file, "r") as f:
        content = f.read()
        assert "BUG: Drops trailing characters" not in content, "The patch was not successfully applied to api_server.cpp."
        assert "out.pop_back()" not in content, "The patch was not successfully applied to api_server.cpp."

def test_server_compiled():
    binary_path = "/home/user/sec_api/build/server"
    assert os.path.isfile(binary_path), f"Compiled server executable {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

def test_response_log():
    log_file = "/home/user/sec_api/response.log"
    assert os.path.isfile(log_file), f"Response log {log_file} is missing."

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_response = "Payload valid and correct"
    assert content == expected_response, f"Response log content is incorrect. Expected '{expected_response}', got '{content}'."