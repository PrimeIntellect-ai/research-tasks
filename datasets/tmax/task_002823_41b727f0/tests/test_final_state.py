# test_final_state.py

import os
import pytest

def test_libprocessor_so_exists():
    so_path = "/home/user/native_module/libprocessor.so"
    assert os.path.isfile(so_path), f"The shared library {so_path} was not created."

    # Check if it's a valid ELF file (shared object)
    with open(so_path, "rb") as f:
        header = f.read(4)
        assert header == b"\x7fELF", f"{so_path} is not a valid ELF file."

def test_process_manifest_script_exists():
    script_path = "/home/user/process_manifest.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_outputs_file_content():
    output_path = "/home/user/outputs.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

    with open(output_path, "r") as f:
        content = f.read().splitlines()

    expected_content = [
        "abc",
        "xyz",
        "helo",
        "build_enginer",
        "consecutive",
        "0"
    ]

    assert content == expected_content, f"The contents of {output_path} do not match the expected output. Got: {content}"