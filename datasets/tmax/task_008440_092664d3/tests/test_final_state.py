# test_final_state.py
import os
import pytest
import hashlib

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def test_result_txt_content():
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"{result_file} does not exist."
    with open(result_file, 'r') as f:
        content = f.read().strip()
    assert content == "MATCH", f"{result_file} contains '{content}', expected 'MATCH'."

def test_merged_bin_matches_reference():
    merged_file = "/home/user/merged.bin"
    ref_file = "/home/user/project_data/reference.bin"

    assert os.path.isfile(merged_file), f"{merged_file} does not exist."
    assert os.path.isfile(ref_file), f"{ref_file} does not exist."

    merged_hash = get_file_hash(merged_file)
    ref_hash = get_file_hash(ref_file)

    assert merged_hash == ref_hash, "The merged.bin file does not match the reference.bin file."

def test_split_files():
    ref_file = "/home/user/project_data/reference.bin"
    assert os.path.isfile(ref_file), f"{ref_file} does not exist."

    split_0 = "/home/user/split_0.bin"
    split_1 = "/home/user/split_1.bin"
    split_2 = "/home/user/split_2.bin"

    assert os.path.isfile(split_0), f"{split_0} does not exist."
    assert os.path.isfile(split_1), f"{split_1} does not exist."
    assert os.path.isfile(split_2), f"{split_2} does not exist."

    assert os.path.getsize(split_0) == 1048576, f"{split_0} size is incorrect."
    assert os.path.getsize(split_1) == 1048576, f"{split_1} size is incorrect."
    assert os.path.getsize(split_2) == 524288, f"{split_2} size is incorrect."

    # Check concatenation
    hasher = hashlib.md5()
    for split_file in [split_0, split_1, split_2]:
        with open(split_file, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

    concat_hash = hasher.hexdigest()
    ref_hash = get_file_hash(ref_file)
    assert concat_hash == ref_hash, "The concatenated split files do not match the reference.bin file."

def test_script_contains_required_modules():
    script_file = "/home/user/organize.py"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."

    with open(script_file, 'r') as f:
        content = f.read()

    assert "fcntl" in content, "The script does not seem to use the 'fcntl' module."
    assert "mmap" in content, "The script does not seem to use the 'mmap' module."