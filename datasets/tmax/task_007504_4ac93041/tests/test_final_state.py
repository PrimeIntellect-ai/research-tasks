# test_final_state.py

import os
import hashlib
import pytest

def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def test_cpp_fixed():
    path = "/home/user/restore_daemon.cpp"
    assert os.path.exists(path), f"{path} missing"
    with open(path, "r") as f:
        content = f.read()
    assert "INADDR_ANY" in content, "C++ code not modified to use INADDR_ANY"
    assert "INADDR_LOOPBACK" not in content, "C++ code still contains INADDR_LOOPBACK"

def test_binary_compiled():
    path = "/home/user/restore_daemon"
    assert os.path.exists(path), f"{path} missing"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_pipeline_script():
    path = "/home/user/pipeline.sh"
    assert os.path.exists(path), f"{path} missing"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_restored_data():
    orig = "/home/user/backup_archive.tar.gz"
    restored = "/home/user/restored_data.bin"
    assert os.path.exists(restored), f"{restored} missing"
    assert get_md5(orig) == get_md5(restored), "Restored data does not match backup archive"

def test_pipeline_result():
    path = "/home/user/pipeline_result.log"
    assert os.path.exists(path), f"{path} missing"
    with open(path, "r") as f:
        content = f.read().strip()
    assert "PIPELINE SUCCESS" in content, f"Expected PIPELINE SUCCESS in {path}"