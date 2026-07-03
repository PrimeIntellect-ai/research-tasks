# test_final_state.py

import os
import pytest

def test_extractor_cpp_exists_and_uses_mmap():
    """Verify that the C++ source file exists and uses mmap."""
    source_path = "/home/user/extractor.cpp"
    assert os.path.isfile(source_path), f"Source file missing at {source_path}"

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "mmap" in content, "The source code must use 'mmap' for memory-mapped I/O."

def test_extracted_files():
    """Verify that base.dat and patch.dat were extracted correctly."""
    base_path = "/home/user/out/base.dat"
    patch_path = "/home/user/out/patch.dat"

    assert os.path.isfile(base_path), f"Extracted file missing: {base_path}"
    assert os.path.isfile(patch_path), f"Extracted file missing: {patch_path}"

    base_size = os.path.getsize(base_path)
    patch_size = os.path.getsize(patch_path)

    assert base_size == 51200, f"base.dat size is {base_size}, expected 51200"
    assert patch_size == 51200, f"patch.dat size is {patch_size}, expected 51200"

def test_restored_file_matches_truth():
    """Verify that restored.dat was reconstructed correctly."""
    restored_path = "/home/user/out/restored.dat"
    truth_path = "/tmp/truth_restored.dat"

    assert os.path.isfile(restored_path), f"Reconstructed file missing: {restored_path}"
    assert os.path.isfile(truth_path), f"Truth file missing: {truth_path}"

    with open(restored_path, "rb") as f:
        restored_data = f.read()

    with open(truth_path, "rb") as f:
        truth_data = f.read()

    assert restored_data == truth_data, "The contents of restored.dat do not match the expected reconstructed data."

def test_zip_slip_prevented():
    """Verify that malicious files were not extracted outside the target directory."""
    evil_sh_path = "/home/user/evil.sh"
    fake_passwd_path = "/etc/fake_passwd"

    assert not os.path.exists(evil_sh_path), f"Zip slip vulnerability detected: {evil_sh_path} was extracted!"
    assert not os.path.exists(fake_passwd_path), f"Zip slip vulnerability detected: {fake_passwd_path} was extracted!"