# test_final_state.py

import os
import sys
import importlib.util

def test_decode_entry_fixed():
    # Load the organizer module dynamically
    spec = importlib.util.spec_from_file_location("organizer", "/home/user/project/organizer.py")
    organizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(organizer)

    # Test UTF-8
    test_str1 = "hello_utf8"
    b1 = test_str1.encode('utf-8')
    data1 = bytes([1]) + len(b1).to_bytes(2, 'little') + b1

    val1, off1 = organizer.decode_entry(data1, 0)
    assert val1 == test_str1, f"Expected {test_str1}, got {val1}"
    assert off1 == len(data1), f"Expected offset {len(data1)}, got {off1}"

    # Test UTF-16LE
    test_str2 = "hello_utf16"
    b2 = test_str2.encode('utf-16le')
    data2 = bytes([2]) + len(b2).to_bytes(2, 'little') + b2

    val2, off2 = organizer.decode_entry(data2, 0)
    assert val2 == test_str2, f"Expected {test_str2}, got {val2}"
    assert off2 == len(data2), f"Expected offset {len(data2)}, got {off2}"

def test_test_organizer_py_exists_and_uses_hypothesis():
    test_path = "/home/user/project/test_organizer.py"
    assert os.path.isfile(test_path), f"{test_path} does not exist"

    with open(test_path, 'r') as f:
        content = f.read()

    assert "test_decode_encode" in content, "test_decode_encode function not found in test_organizer.py"
    assert "hypothesis" in content, "hypothesis library not imported/used in test_organizer.py"
    assert "strategies.text" in content or "st.text" in content, "hypothesis text strategy not used"
    assert "sampled_from" in content, "hypothesis sampled_from strategy not used"

def test_mem_peak_txt_exists_and_valid():
    mem_path = "/home/user/mem_peak.txt"
    assert os.path.isfile(mem_path), f"{mem_path} does not exist"

    with open(mem_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"{mem_path} does not contain a valid integer: '{content}'"

def test_organized_files_txt_correct():
    out_path = "/home/user/organized_files.txt"
    assert os.path.isfile(out_path), f"{out_path} does not exist"

    expected_files = [
        "CMakeLists.txt",
        "build/config.h",
        "include/utils.hpp",
        "lib/libUTF16_test.so",
        "lib/libmath.so",
        "src/main.cpp"
    ]

    with open(out_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_files, f"Contents of {out_path} are incorrect. Expected {expected_files}, got {lines}"