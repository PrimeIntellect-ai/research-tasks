# test_final_state.py

import os
import pytest

def test_output_txt_content():
    output_path = "/home/user/workspace/output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing. Did you run your Go program and write the output?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "30", f"Expected output.txt to contain '30', but found '{content}'"

def test_fix_patch_exists_and_valid():
    patch_path = "/home/user/workspace/fix.patch"
    assert os.path.isfile(patch_path), f"{patch_path} is missing. Did you generate the diff?"

    with open(patch_path, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"{patch_path} does not appear to be a valid unified diff patch file."
    assert "processor.go" in content, f"{patch_path} does not appear to contain diffs for processor.go."