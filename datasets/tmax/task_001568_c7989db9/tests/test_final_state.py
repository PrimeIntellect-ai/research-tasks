# test_final_state.py

import os
import pytest

def test_libprocess_so_exists():
    """Test that the shared library was built."""
    assert os.path.isfile("/home/user/libprocess.so"), "libprocess.so was not built. Did you run 'make'?"

def test_output_file_exists():
    """Test that the output file was generated."""
    assert os.path.isfile("/home/user/output.txt"), "output.txt was not generated. Did you run the python script?"

def test_output_file_content():
    """Test that the output file exactly matches the expected bytes."""
    expected_path = "/home/user/expected.txt"
    output_path = "/home/user/output.txt"

    assert os.path.isfile(expected_path), f"Missing {expected_path}"
    assert os.path.isfile(output_path), f"Missing {output_path}"

    with open(expected_path, "rb") as f:
        expected_content = f.read()

    with open(output_path, "rb") as f:
        output_content = f.read()

    assert output_content == expected_content, (
        f"Output content does not match expected. "
        f"Expected {expected_content}, got {output_content}. "
        "Check your encoding/decoding logic in process.py."
    )

def test_process_py_uses_latin1():
    """Test that process.py was modified to use latin-1 for encoding and decoding."""
    with open("/home/user/process.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "encode('latin-1')" in content or 'encode("latin-1")' in content, "process.py does not encode using latin-1"
    assert "decode('latin-1')" in content or 'decode("latin-1")' in content, "process.py does not decode using latin-1"