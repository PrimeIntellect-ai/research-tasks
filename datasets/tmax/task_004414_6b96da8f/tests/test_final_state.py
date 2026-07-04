# test_final_state.py
import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/archive_docs"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"Executable {executable_path} is not executable."

def test_manifest_content():
    manifest_path = "/home/user/docs_output/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/docs_input/module_a/intro.txt",
        "/home/user/docs_input/module_b/submodule/details.txt",
        "/home/user/docs_input/module_c/long.txt"
    ]

    assert lines == expected_lines, f"Manifest contents do not match expected sorted unique absolute paths. Got: {lines}"

def test_chunk_content():
    chunk_path = "/home/user/docs_output/chunk_0000.dat"
    assert os.path.isfile(chunk_path), f"Chunk file {chunk_path} is missing."

    with open(chunk_path, "rb") as f:
        data = f.read()

    expected_data = bytes([
        0x05, ord('A'),
        0x05, ord('B'),
        0x05, ord('C'),
        0x05, ord('D'),
        0x05, ord('E'),
        0x05, ord('F'),
        0xFF, ord('G'),
        0x2D, ord('G')
    ])

    assert data == expected_data, f"Chunk data does not match expected RLE byte stream. Got: {data.hex()}"

def test_no_extra_chunks():
    output_dir = "/home/user/docs_output"
    chunk_files = [f for f in os.listdir(output_dir) if f.startswith("chunk_") and f.endswith(".dat")]

    assert len(chunk_files) == 1, f"Expected exactly 1 chunk file, but found {len(chunk_files)}: {chunk_files}"
    assert chunk_files[0] == "chunk_0000.dat", f"Unexpected chunk file name: {chunk_files[0]}"