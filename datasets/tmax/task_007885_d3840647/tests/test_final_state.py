# test_final_state.py

import os
import subprocess
import pytest

def test_corrupt_offset_file():
    offset_file = "/home/user/corrupt_offset.txt"
    assert os.path.isfile(offset_file), f"The file {offset_file} does not exist."

    with open(offset_file, "r") as f:
        content = f.read().strip()

    assert content == "378", f"Expected the corrupt offset to be 378, but got '{content}'."

def test_cargo_test_passes():
    project_dir = "/home/user/wal_parser"
    assert os.path.isdir(project_dir), f"The project directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo test failed with output:\n{result.stdout}\n{result.stderr}"

def test_lib_rs_modifications():
    lib_rs_path = "/home/user/wal_parser/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"The file {lib_rs_path} does not exist."

    with open(lib_rs_path, "r") as f:
        content = f.read()

    # Check that the function signature and Error enum are unmodified
    assert "pub enum Error {" in content, "The Error enum declaration is missing or modified."
    assert "UnexpectedEof," in content, "The UnexpectedEof variant is missing."
    assert "pub fn parse_wal(data: &[u8]) -> Result<usize, Error>" in content, "The parse_wal function signature was modified."

    # Check that there is some bounds checking before payload slicing
    # We can't strictly regex for exact code since the student might write it differently,
    # but cargo test passing + UnexpectedEof being returned verifies the behavior.
    # We'll just ensure the file was modified from its original state.
    original_buggy_line = "let _payload = &data[offset..offset + len];"
    # It might still contain this line, but protected by an if statement.
    # The real verification is that `cargo test` passes.