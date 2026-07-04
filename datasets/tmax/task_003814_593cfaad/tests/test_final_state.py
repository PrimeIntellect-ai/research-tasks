# test_final_state.py

import os
import pytest

def test_assembler_cpp_exists_and_contains_required_headers():
    """Test that assembler.cpp exists and includes required headers."""
    cpp_path = "/home/user/assembler.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with open(cpp_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_traversal = ("<dirent.h>" in content) or ("<filesystem>" in content)
    has_fstream = "<fstream>" in content

    assert has_traversal, "assembler.cpp must include <dirent.h> or <filesystem> for directory traversal."
    assert has_fstream, "assembler.cpp must include <fstream> for file I/O operations."

def test_assembler_executable_exists():
    """Test that the compiled assembler executable exists."""
    exe_path = "/home/user/assembler"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_reassembled_tarball_exists():
    """Test that the reassembled tarball exists and has gzip magic bytes."""
    tarball_path = "/home/user/reassembled_project.tar.gz"
    assert os.path.isfile(tarball_path), f"Reassembled tarball {tarball_path} does not exist."

    with open(tarball_path, 'rb') as f:
        magic = f.read(2)
    assert magic == b'\x1f\x8b', f"{tarball_path} does not appear to be a valid gzip file."

def test_manifest_txt_exists():
    """Test that manifest.txt was extracted."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Extracted manifest {manifest_path} does not exist."

def test_manifest_summary_content():
    """Test that manifest_summary.txt contains the correct first line."""
    summary_path = "/home/user/manifest_summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_content = "PROJECT_ID: ALPHA_7782_OMEGA\n"
    assert content == expected_content, f"manifest_summary.txt content is incorrect. Expected: {repr(expected_content)}, Got: {repr(content)}"