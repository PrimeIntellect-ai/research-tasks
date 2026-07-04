# test_final_state.py

import os
import subprocess
import time
import hashlib
import shutil
import pytest

def test_pack_manager_binary():
    """Check if the pack_manager binary exists and is executable."""
    binary_path = "/home/user/pack_manager"
    assert os.path.exists(binary_path), f"{binary_path} does not exist. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_pack_mode():
    """Test the pack mode of the utility."""
    test_dir = "/home/user/test_pack"
    os.makedirs(os.path.join(test_dir, "nested"), exist_ok=True)
    with open(os.path.join(test_dir, "file1.txt"), "w") as f:
        f.write("hello")
    with open(os.path.join(test_dir, "nested", "file2.txt"), "w") as f:
        f.write("world")

    out_file = "/home/user/test.cfgpack"
    if os.path.exists(out_file):
        os.remove(out_file)

    result = subprocess.run(["/home/user/pack_manager", "pack", test_dir, out_file], capture_output=True)
    assert result.returncode == 0, f"pack_manager pack failed: {result.stderr.decode()}"
    assert os.path.exists(out_file), "test.cfgpack was not created by pack_manager"

    with open(out_file, "rb") as f:
        content = f.read()

    assert b"MANIFEST_START\n" in content, "Missing MANIFEST_START"
    assert b"MANIFEST_END\n" in content, "Missing MANIFEST_END"
    assert b"DATA_START\n" in content, "Missing DATA_START"
    assert b"DATA_END\n" in content, "Missing DATA_END"

    # Check hashes in manifest
    # hello: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
    # world: 486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7
    assert b"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824" in content, "Missing correct SHA-256 for file1.txt"
    assert b"486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7" in content, "Missing correct SHA-256 for file2.txt"

def test_watch_mode_success():
    """Test the watch mode extraction and logging on success."""
    res = subprocess.run(["pgrep", "pack_manager"], capture_output=True)
    assert res.returncode == 0, "pack_manager is not running in the background"

    out_file = "/home/user/test.cfgpack"
    dropzone = "/home/user/dropzone"
    configs = "/home/user/configs"

    os.makedirs(dropzone, exist_ok=True)
    os.makedirs(configs, exist_ok=True)

    shutil.copy(out_file, os.path.join(dropzone, "test.cfgpack"))

    # Wait for inotify event and processing
    time.sleep(2)

    assert os.path.exists(os.path.join(configs, "file1.txt")), "file1.txt was not extracted"
    assert os.path.exists(os.path.join(configs, "nested", "file2.txt")), "nested/file2.txt was not extracted"

    with open(os.path.join(configs, "file1.txt"), "r") as f:
        assert f.read() == "hello", "Extracted content for file1.txt is incorrect"

    log_file = "/home/user/manager.log"
    assert os.path.exists(log_file), "manager.log does not exist"
    with open(log_file, "r") as f:
        log_content = f.read()

    assert "[ARCHIVE EVENT]" in log_content, "Missing [ARCHIVE EVENT] in log"
    assert "File: test.cfgpack" in log_content, "Missing File log entry for test.cfgpack"
    assert "Status: SUCCESS" in log_content, "Missing Status: SUCCESS in log"
    assert "Files Processed: 2" in log_content, "Missing Files Processed: 2 in log"

def test_watch_mode_malicious():
    """Test the watch mode behavior on a malicious archive (Zip Slip attempt)."""
    malicious_file = "/home/user/malicious.cfgpack"
    dropzone = "/home/user/dropzone"

    content = b"evil"
    h = hashlib.sha256(content).hexdigest()

    with open(malicious_file, "wb") as f:
        f.write(b"MANIFEST_START\n")
        f.write(f"../evil.txt|4|{h}\n".encode())
        f.write(b"MANIFEST_END\n")
        f.write(b"DATA_START\n")
        f.write(content)
        f.write(b"DATA_END\n")

    shutil.copy(malicious_file, os.path.join(dropzone, "malicious.cfgpack"))

    # Wait for inotify event and processing
    time.sleep(2)

    assert not os.path.exists("/home/user/evil.txt"), "Path traversal vulnerability detected! Malicious file was extracted."

    log_file = "/home/user/manager.log"
    with open(log_file, "r") as f:
        log_content = f.read()

    assert "File: malicious.cfgpack" in log_content, "Missing File log entry for malicious.cfgpack"
    assert "Status: ERROR_PATH_TRAVERSAL" in log_content, "Missing Status: ERROR_PATH_TRAVERSAL in log"
    assert "Files Processed: 0" in log_content, "Missing Files Processed: 0 in log for malicious file"