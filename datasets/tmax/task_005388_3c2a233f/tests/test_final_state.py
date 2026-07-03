# test_final_state.py

import os
import subprocess
import pytest

def test_bad_signature_txt():
    path = "/home/user/bad_signature.txt"
    assert os.path.isfile(path), f"{path} is missing"

    with open(path, "r") as f:
        content = f.read().strip()

    # Remove whitespace and normalize to uppercase
    normalized_content = "".join(content.split()).upper()
    assert normalized_content == "DEADBEEF", f"{path} does not contain the correct 4-byte sequence"

def test_fuzzer_py_exists():
    path = "/home/user/fuzzer.py"
    assert os.path.isfile(path), f"{path} is missing"

def test_mre_py_segfaults():
    path = "/home/user/mre.py"
    assert os.path.isfile(path), f"{path} is missing"

    # Run mre.py and check for segmentation fault
    result = subprocess.run(["python3", path], capture_output=True)

    # A segmentation fault typically results in return code 139 or -11 in Python's subprocess
    assert result.returncode in (139, -11), f"{path} did not result in a segmentation fault (return code: {result.returncode})"

def test_safe_report_generator_py_exists():
    path = "/home/user/safe_report_generator.py"
    assert os.path.isfile(path), f"{path} is missing"

def test_processed_log():
    path = "/home/user/app/processed.log"
    assert os.path.isfile(path), f"{path} is missing. Make sure safe_report_generator.py was run successfully."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "Processed 1000 chunks" in content, f"{path} does not contain the expected success message"